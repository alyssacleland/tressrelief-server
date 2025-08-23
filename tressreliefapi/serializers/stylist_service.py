from rest_framework import serializers
from tressreliefapi.models import StylistService


class StylistServiceSerializer(serializers.ModelSerializer):
    """JSON Serializer for stylist_service join table"""

    class Meta:
        model = StylistService
        fields = ('id', 'stylist', 'service')
        read_only_fields = ('id')
