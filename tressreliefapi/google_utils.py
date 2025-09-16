# Access tokens only last an hour, so will need to use the refresh token to get new access tokens when they expire. This helper will make sure tokens are valid before any google api request.

# DOCS: Refrshing an access token (offline access): https://developers.google.com/identity/protocols/oauth2/web-server#offline

import datetime
import requests
from tressreliefapi.models.oauth_credential import OAuthCredential
from django.conf import settings
from django.utils import timezone


def get_valid_access_token(user):
    """ Ensure the stylist has a valid Google access token. 
    Refresh if expired, then return the token."""

    # 1.) Look up the stylit's OAuthCredential
    try:
        credential = OAuthCredential.objects.get(user=user, provider='google')
    except OAuthCredential.DoesNotExist:
        return None  # stylist hasn't connected their google account yet

    # 2.) Check if token_expiry is in the valid still (if it is greater than 'now'), if so return the access token
    if credential.token_expiry and credential.token_expiry > timezone.now():
        return credential.access_token

    # 3.) othwerwise (if token_expiry is in the past (invalid)), call google's token refresh endpoint with the stored refresh_token (docs linked above).
    else:
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,  # from google cloud
            "client_secret": settings.GOOGLE_CLIENT_SECRET,  # from google cloud
            # tells google what kind of exchange this is, docs say it must be this value
            "grant_type": 'refresh_token',
            "refresh_token": credential.refresh_token,
        }
        response = requests.post(
            # the following returns json with new access token and expiry time if successful
            'https://oauth2.googleapis.com/token', data=data)
        if response.status_code != 200:  # if refresh failed
            return None
        else:  # refresh successful
            tokens = response.json()

            credential.access_token = tokens["access_token"]
            # default to 1 hour if missing
            expires_in = tokens.get("expires_in", 3600)
            credential.token_expiry = timezone.now() + datetime.timedelta(seconds=expires_in)
    # 4.) (cont on step 3) save the new access token and expiry time back to the DB
            credential.save()
    # 5.) return valid access token for use in future api calls
            return credential.access_token
