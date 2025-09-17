# endpoints to get appointment availability for a given service on a given date by stylists who offer that service (and optional stylist filter)
# aka... For Service X on Date Y, what slots are open across the stylists who offer that service?
# DOCS: https://developers.google.com/workspace/calendar/api/v3/reference/freebusy/query

import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_date  # to parse date from query param
from tressreliefapi.models import Service, StylistService, UserInfo
from tressreliefapi.models.oauth_credential import OAuthCredential
from tressreliefapi.utils.availability import generate_available_slots
from tressreliefapi.utils.google_utils import get_valid_access_token
from dateutil.parser import isoparse

# GET /services/:<service_id>/availability/?date=YYYY-MM-DD&stylist_id=:<stylist_id> (stylist_id is optional)


@api_view(['GET'])
def service_availability(request, id):
    """
    Get available appointment slots for a given service on a given date.
    Query params:
    - date (required): date in YYYY-MM-DD format
    - stylist_id (optional): filter slots to a specific stylist
    """
    # 1.) get data and stylist_id (if provided) from query params
    date_str = request.query_params.get('date')
    stylist_id = request.query_params.get('stylist_id')

    # parse and validate date
    date = parse_date(date_str)

    if not date:
        return Response({"error": "Valid date query param is required (YYYY-MM-DD)."}, status=400)

    # 2.) look up the service by id
    service = Service.objects.get(pk=id)

    # 3.) Lookup stylists linked to the service via Stylist_Service
    service_stylist_links = StylistService.objects.filter(service=service)
    # 4.) if stylist_id provided, filter to links of that stylist only
    if stylist_id:
        service_stylist_links = service_stylist_links.filter(
            stylist__id=stylist_id)

    # 5.) for each stylist, get their availability for that date (using helper function that calls google calendar api)
    availability = []
    for link in service_stylist_links:
        stylist = link.stylist
        # Get access token for the stylist
        access_token = get_valid_access_token(stylist)
        if not access_token:
            continue  # stylist hasn't connected their google calendar yet, skip them

        # DEBUG: list all events for this stylist on that date
        response = requests.get(
            "https://www.googleapis.com/calendar/v3/calendars/primary/events",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "timeMin": f"{date.isoformat()}T00:00:00Z",
                "timeMax": f"{date.isoformat()}T23:59:59Z",
                "singleEvents": True,
                "orderBy": "startTime"
            }
        )
        print("Events raw:", response.json())

        credential = OAuthCredential.objects.filter(
            user=stylist, provider="google").first()
        print("DEBUG stylist_id:", stylist.id, "google_email:", stylist.google_email,
              "oauth_user_id:", credential.user_id if credential else None)

        # call freebusy api
        # DOCS: https://developers.google.com/workspace/calendar/api/v3/reference/freebusy/query
        # we basically tell freebusy: Between X and Y, tell me the busy chunks for calendar Z. and it returns an array of busy chunks (start and end times).

        # want the whole day in UTC to make sure we get all busy times that day. generate_available_slots() will handle converting to CST and enforcing working hours.
        # start of day (midnight) in UTC
        start_of_day = f"{date.isoformat()}T00:00:00Z"
        # end of day (11:59:59pm) in UTC
        end_of_day = f"{date.isoformat()}T23:59:59Z"

        # what the freebusy api expects in the body of the post request
        body = {
            "timeMin": start_of_day,
            "timeMax": end_of_day,
            # primary calendar of the authenticated user
            "items": [{"id": "primary"}]
        }

        response = requests.post(
            # freebusy endpoint
            "https://www.googleapis.com/calendar/v3/freeBusy",
            # bearer means whoever presents this is the "bearer" and is granted access. no other auth needed.
            # send the access token we got for the stylist in the auth header so we can see their calendar
            headers={"Authorization": f"Bearer {access_token}"},
            # this runs json.dumps() for us and sets content-type to application/json
            json=body,
        )
        if response.status_code != 200:
            continue  # skip this stylist if api call failed

        print("FreeBusy raw:", response.json())

        # parse the response to get busy intervals. .json() parses json string into a python dict
        busy_raw = response.json()["calendars"]["primary"]["busy"]
        busy_intervals = [(isoparse(b["start"]), isoparse(b["end"]))
                          for b in busy_raw]

        # Generate available slots (apply salon hours + slice into bookable chunks)
        slots = generate_available_slots(
            service.duration, busy_intervals, date)

        # Add this stylist’s availability to results
        availability.append({
            "stylist_id": stylist.id,
            "stylist_name": stylist.display_name,
            "slots": slots  # these are still in UTC, FE can convert back to CT when displaying
        })

    # 5. Return JSON array of stylists + their slots
    return Response(availability)
