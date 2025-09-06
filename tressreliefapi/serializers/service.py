from rest_framework import serializers
from tressreliefapi.models import Category, Service


class ServiceSerializer(serializers.ModelSerializer):
    """JSON Serializer for services"""

    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'category', 'duration',
                  'price', 'image_url', 'active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
