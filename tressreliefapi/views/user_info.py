"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tressreliefapi.models import UserInfo
from tressreliefapi.serializers import UserInfoSerializer


class UserInfoView(ViewSet):
    """Tress Relief UserInfo view"""

    def list(self, request):
        """Handle GET requests for UserInfo
        You can filter with ?role=stylist, ?role=admin, or ?role=client
        """

        # get all the userinfos
        userinfos = UserInfo.objects.all()

        # filter by role if provided
        role = request.query_params.get('role', None)
        if role is not None:
            userinfos = userinfos.filter(role=role)

        serializer = UserInfoSerializer(userinfos, many=True)
        return Response(serializer.data)
