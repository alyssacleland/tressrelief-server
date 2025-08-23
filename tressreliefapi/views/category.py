"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tressreliefapi.models import Category
from tressreliefapi.serializers import CategorySerializer


class CategoryView(ViewSet):

    # /categories
    def list(self, request):
        """
        Handle GET requests for categories
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # /categories/:id
    def retrieve(self, request, pk):
        """Handle GET requests for single category"""
        category = Category.objects.get(pk=pk)
        try:
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
