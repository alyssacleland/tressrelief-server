"""View module for handling requests about services"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tressreliefapi.models import Service, Category
from tressreliefapi.serializers import ServiceSerializer


class ServiceView(ViewSet):

    # /services, /services?category=:id, /services?stylistId=:id
    def list(self, request):
        """
        Handle GET requests for services
        """
        services = Service.objects.all()

        # filter by category id if provided
        category = request.query_params.get('categoryId', None)
        if category is not None:
            services = services.filter(category=category)

        # list the services offered by a stylist
        # filter by stylistId via join table (StylistService... related_name="service_stylists")
        stylist_id = request.query_params.get('stylistId')
        if stylist_id:
            # filter by the services where the stylist on join table row equals the stylist in the query param
            services = services.filter(service_stylists__stylist_id=stylist_id)

        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)

    # /services/:id

    def retrieve(self, request, pk):
        """Handle GET requests for single service"""
        try:
            service = Service.objects.get(pk=pk)
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        except Service.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
