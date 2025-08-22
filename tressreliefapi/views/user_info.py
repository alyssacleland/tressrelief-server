"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tressreliefapi.models import UserInfo
from tressreliefapi.serializers import UserInfoSerializer


class UserInfoView(ViewSet):
    """Tress Relief UserInfo view"""

    # /userinfo, /userinfo?role=:role
    def list(self, request):
        """Handle GET requests for UserInfo
        You can list all and filter with ?role=stylist, ?role=admin, or ?role=client
        """

        # get all the userinfos
        userinfos = UserInfo.objects.all()

        # filter by role if provided
        role = request.query_params.get('role', None)
        if role is not None:
            userinfos = userinfos.filter(role=role)

        serializer = UserInfoSerializer(userinfos, many=True)
        return Response(serializer.data)

    # /userinfo/:id
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single userinfo by id"""
        try:
            userinfo = UserInfo.objects.get(pk=pk)
        except UserInfo.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserInfoSerializer(userinfo)
        return Response(serializer.data)
