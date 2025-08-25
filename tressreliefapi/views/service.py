"""View module for handling requests about services"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tressreliefapi.models import Service, Category, StylistService, UserInfo
from tressreliefapi.serializers import ServiceSerializer, UserInfoSerializer
from rest_framework.decorators import action


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

    # /services
    def create(self, request):
        """Handle POST operations"""
        category = Category.objects.get(pk=request.data["category"])

        service = Service.objects.create(
            category=category,
            name=request.data["name"],
            description=request.data["description"],
            duration=request.data["duration"],
            price=request.data["price"],
            # default to empty string if not provided. model allows empty with blank=True
            image_url=request.data.get("image_url", ""),
            active=request.data.get("active", True)
            # leave out created_at and updated_at because they are set automatically via my model definition
        )
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # /services/:id
    def update(self, request, pk):
        """Handle PUT requests for a service"""
        try:
            service = Service.objects.get(pk=pk)
            service.category = Category.objects.get(
                pk=request.data["category"])
            service.name = request.data["name"]
            service.description = request.data["description"]
            service.duration = request.data["duration"]
            service.price = request.data["price"]
            service.image_url = request.data.get("image_url", "")
            service.active = request.data.get("active", True)
            service.save()
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        except Service.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # /services/:id
    def destroy(self, request, pk):
        """Handle DELETE requests for a service"""
        try:
            service = Service.objects.get(pk=pk)
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Service.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # get stylists of a service
    # /services/:id/stylists
    # with the action decorator, the router you already registered will auto‑create the URL route stylists
    @action(methods=['get'], detail=True)
    def stylists(self, request, pk):
        """Handle GET requests for stylists of a service"""
        try:
            service = Service.objects.get(pk=pk)
            # find all join rows for this service
            stylist_links = StylistService.objects.filter(service=service)
            # get all stylists (UserInfo objs) from the join rows
            stylists = [link.stylist for link in stylist_links]
            serializer = UserInfoSerializer(stylists, many=True)
            return Response(serializer.data)
        except Service.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # /services/:id/add_stylist
    @action(methods=['post'], detail=True)
    def add_stylist(self, request, pk):
        """Handle POST requests to add a stylist to a service"""
        try:
            service = Service.objects.get(pk=pk)
            stylist = UserInfo.objects.get(pk=request.data["stylist"])
            obj, created = StylistService.objects.get_or_create(
                service=service, stylist=stylist)
            if not created:
                return Response({'message': 'Stylist already offers this service'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        except (Service.DoesNotExist, UserInfo.DoesNotExist) as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    # /services/:id/remove_stylist/stylistId=:id
    @action(methods=['delete'], detail=True)
    def remove_stylist(self, request, pk):
        """Handle DELETE requests to remove a stylist from a service"""
        # get the stylistId from the query params
        stylist_id = request.query_params.get("stylistId", None)
        if stylist_id is None:
            return Response({'message': 'Missing stylistId query parameter'}, status=status.HTTP_400_BAD_REQUEST)
        # delete the link row
        try:
            link = StylistService.objects.get(stylist=stylist_id, service=pk)
            link.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StylistService.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
