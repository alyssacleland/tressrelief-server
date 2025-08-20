from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tressreliefapi.models import UserInfo
from tressreliefapi.serializers import UserInfoSerializer


@api_view(["POST"])
def get_or_create_user(request):
    """
    Body:
      {
        "uid": "<firebase uid>",
        "display_name": "<optional>",
        "google_email": "<optional>"
      }
    Returns the existing user or creates one with role='client'.
    """
    uid = request.data.get("uid")
    if not uid:
        return Response({"detail": "Missing uid"}, status=status.HTTP_400_BAD_REQUEST)

    defaults = {
        "display_name": request.data.get("display_name") or "",
        "google_email": request.data.get("google_email") or "",
    }

    user, _ = UserInfo.objects.get_or_create(uid=uid, defaults=defaults)
    return Response(UserInfoSerializer(user).data, status=status.HTTP_200_OK)
