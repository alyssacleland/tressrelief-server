from rest_framework import serializers
from tressreliefapi.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """JSON Serializer for categories"""

    class Meta:
        model = Category
        fields = ('id', 'name', 'description',
                  'image_url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
