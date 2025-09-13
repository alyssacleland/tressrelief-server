from urllib.parse import urlencode
from django.conf import settings
from django.http import JsonResponse

# DOCS: https://developers.google.com/identity/protocols/oauth2/web-server

SCOPES = [
    # needed to create/update/delete events on stylist's calendar
    "https://www.googleapis.com/auth/calendar.events",
    # needed to read the stylist's busy times to generate availability
    "https://www.googleapis.com/auth/calendar.readonly",
]

# /oauth/google/initiate/


def oauth_google_initiate(request):
    """ Initiate the OAuth2 flow by redirecting to Google's OAuth 2.0 server
        to obtain user consent for the requested scopes.
        Returns a JSON response containing the URL to redirect the user to."""
    params = {
        # OAuth client ID i got from google cloud
        "client_id": settings.GOOGLE_CLIENT_ID,
        # matches what i set in google cloud
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        # we want an authorization code back (this will be used in the callback url we redirect to, to get access/refresh tokens)
        "response_type": "code",
        # URL-encoded list of permissions... here we want calendar access. these values inform the consent screen the user sees
        "scope": " ".join(SCOPES),
        # we want a refresh token ("Indicates whether your application can refresh access tokens when the user is not present at the browser.")
        "access_type": "offline",
        # forces the consent screen to always show (to get refresh token each time)
        "prompt": "consent",
    }
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return JsonResponse({"url": url})

# google consent url structure (example):
# https://accounts.google.com/o/oauth2/v2/auth?
# client_id=110025474277-rp86u96j9pplrmma9aknmegc1ongn48p.apps.googleusercontent.com
# &redirect_uri=http://localhost:8000/oauth/google/callback/
# &response_type=code
# &scope=https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/calendar.readonly
# &access_type=offline
# &include_granted_scopes=true
# &prompt=consent

# front-end will call this endpoint (when a stylist clicks a button to connect their Google Calendar), get back the conxsent url, and redirect the stylist to it
# stylist will log in to google and approve the requested permissions
# after the user clicks allow, then google will redirect to my redirect uri (which i set in google cloud console), which i will make an endpoint for next
