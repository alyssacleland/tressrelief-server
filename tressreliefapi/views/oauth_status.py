# get whether stylist has connected their google calendar (for use in FE to show connected state vs connect button)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tressreliefapi.models.oauth_credential import OAuthCredential
from tressreliefapi.models.user_info import UserInfo

# http://localhost:8000/oauth/google/status
# (include in headerL: Authorization: <stylist uid>)


@api_view(['GET'])
def oauth_google_status(request):
    """Return whether stylist has connected their Google Calendar"""
    # for now, assume user is the first stylist in the db (later (TODO:) will get user from auth token in request header)
    uid = request.headers.get("Authorization")
    if not uid:
        return Response({"error": "Missing Authorization header"}, status=status.HTTP_401_UNAUTHORIZED)

  # look up user by uid
    try:
        user = UserInfo.objects.get(uid=uid)
    except UserInfo.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

  # goal is that only stylists can connect google calendar, but for now i only protect that on the frontend (later TODO:)

  # look up OAuthCredential for this user and return whether it exists as true (including calendar_id and updated_at) or false (if it does, they have connected their calendar)
    try:
        cred = OAuthCredential.objects.get(user=user, provider="google")
        return Response({
            "connected": True,
            "calendar_id": cred.calendar_id,
            "updated_at": cred.token_expiry
        })
    except OAuthCredential.DoesNotExist:
        return Response({"connected": False})
