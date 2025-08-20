from rest_framework import serializers
from models import UserInfo


class UserInfoSerializer(serializers.ModelSerialzier):
    """JSON Serializer for user info"""
    class Meta:
        model = UserInfo
        fields = ("id", "uid", "display_name", "google_email",
                  "role", "created_at", "updated_at")
        # Fields listed in read_only_fields will be returned in responses but ignored on incoming writes. Mark server-managed stuff (PK and timestamps) as read-only so clients can’t set them.
        read_only_fields = ("id", "created_at", "updated_at")
