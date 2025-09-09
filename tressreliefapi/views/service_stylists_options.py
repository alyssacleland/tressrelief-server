from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Exists, OuterRef, BooleanField, Value
from tressreliefapi.models import UserInfo, StylistService


# GET /service-stylist-options?serviceId=:id
# list all stylists and whether they offer the given service (joined is True if they offer the service)
# for prefilling stylists in the edit form
class ServiceStylistOptions(APIView):
    """
    GET /service-stylist-options?serviceId=:id

    Returns all stylists (UserInfo where role="stylist") and, for each stylist,
    a boolean 'joined' that is True if they already offer the given service.

    If serviceId is omitted, joined=False for all stylists.
    """

    def get(self, request):
        service_id = request.query_params.get("serviceId")

        # start with all stylists (outer query)
        # outer query is the qs you call annotate on
        # The “subquery” is any QuerySet you wrap in Exists() (or Subquery) and pass into annotate()
        stylists = UserInfo.objects.filter(
            role="stylist").order_by("display_name", "id")

        if service_id:  # (update)
            link_exists = StylistService.objects.filter(
                service_id=service_id,
                # OuterRef("pk"): tells Django, “inside the subquery, use the current outer row’s primary key.” That’s what makes it a correlated subquery (evaluated per stylist).
                stylist_id=OuterRef("pk"),
            )
            # The exists operator is used to test for the existence of any record in a subquery. The exists operator returns true here if the subquery returns one or more records.
            stylists = stylists.annotate(joined=Exists(link_exists))
        else:  # (create)
            stylists = stylists.annotate(joined=Value(
                False, output_field=BooleanField()))

        data = list(
            stylists.values("id", "display_name",
                            "google_email", "photo_url", "joined")
        )
        return Response(data, status=status.HTTP_200_OK)
