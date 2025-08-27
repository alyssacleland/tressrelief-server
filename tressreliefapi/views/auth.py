from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tressreliefapi.models import UserInfo
from tressreliefapi.serializers import UserInfoSerializer

# /get-or-create-user


@api_view(["POST"])
def get_or_create_user(request):
    """
    Body:
      {
        "uid": "<firebase uid>",
        "display_name": "<optional>",
        "google_email": "<optional>",
        "photo_url": "<optional>"
      }
    Returns the existing user or creates one with role='client'.
    """
    uid = request.data.get("uid")
    if not uid:
        return Response({"detail": "Missing uid"}, status=status.HTTP_400_BAD_REQUEST)

    defaults = {
        "display_name": request.data.get("display_name") or "",
        "google_email": request.data.get("google_email") or "",
        "photo_url": request.data.get("photo_url") or None,
    }

    user, created = UserInfo.objects.get_or_create(uid=uid, defaults=defaults)
    if not created:
        changed = False
        for field in ("display_name", "google_email", "photo_url"):
            incoming = request.data.get(field, None)
            if incoming is not None and incoming != getattr(user, field):
                setattr(user, field, incoming)
                changed = True

        if changed:
            user.save()

    return Response(UserInfoSerializer(user).data, status=status.HTTP_200_OK)
