# this is the endpoint that google will redirect to after the user consents (or doesn't) from the oauth_google_initiate view
# i will need to exchange the authorization code that google sends me for access and refresh tokens

# DOCS: https://developers.google.com/identity/protocols/oauth2/web-server#exchange-authorization-code

from urllib import request
import requests
from rest_framework.response import Response
from rest_framework import status
from tressreliefproject import settings
from django.utils import timezone
from datetime import timedelta
from models.user_info import UserInfo
from models.oauth_credential import OauthCredential


@api_view(['GET'])
def oauth_google_callback(request):
    """ 
    handles googled redirect with ?code=...
    Exchanges the code for tokens and saves them in OauthCredential model 
    """

    # 1. Grab the code that Google sends me in the query parameters
    code = request.query_params.get("code")
    if not code:
        return Response({"error": "Missing Code"}, status=status.HTTP_400_BAD_REQUEST)

    # 2. Exchange the code for tokens
    # DOCS: https://developers.google.com/identity/protocols/oauth2/web-server#httprest_3
    # https://datatracker.ietf.org/doc/html/rfc6749#section-4.1.3

    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,  # short-lived authorization code from query param, proves user consented
        "client_id": settings.GOOGLE_CLIENT_ID,  # from google cloud
        "client_secret": settings.GOOGLE_CLIENT_SECRET,  # from google cloud
        # matches what i set in google cloud
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        # tells google what kind of exchange this is, docs say to use this value
        "grant_type": "authorization_code",  # standard for web apps
    }

    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return Response({"error": "Failed to exchange code for tokens"}, status=status.HTTP_400_BAD_REQUEST)

    token_data = response.json()  # should contain access_token, expires_in, refresh_token, scope, token_type, id_token (this is what is returned according to docs: https://developers.google.com/identity/protocols/oauth2/web-server#httprest_3)

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")  # in seconds

    expiry = timezone.now() + timezone.timedelta(seconds=expires_in)

    # 3. for now, assume current user is the first stylist in the db (later (TODO) will get user from auth token in request header)
    # first() gets the first object in the queryset
    stylist = UserInfo.objects.filter(role="stylist").first()
    if not stylist:
        return Response({"error": "No stylist found"}, status=status.HTTP_400_BAD_REQUEST)

    # 4. TODO: Save in DB
    # The update_or_create method returns a tuple (obj, created) , where obj in the object, and created is a boolean showing whether a new object was created.
    credentials, created = OauthCredential.objects.update_or_create(
        user=stylist,
        provider='google',
        defaults={
            'access_token': access_token,
            'token_expiry': expiry,
            # only save refresh_token if present. google someties doesn't send it if the user has already connected before. don't overwrite an existing refresh token with None!
            # ** is like the spread operator in js, it spreads the key/value pairs of an object into another object
            **({'refresh_token': refresh_token} if 'refresh_token' else {}),
            'calendar_id': 'primary'
        }
    )

    # 5. TODO: send a response back to the front-end (maybe just a success message for now) (later (TODO) may redirect front-end)
