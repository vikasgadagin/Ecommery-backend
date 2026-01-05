from unicodedata import name
from uuid import UUID

from django.forms.fields import UUIDField
from rest_framework import viewsets, serializers, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

import category
from .serializers import *

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        name=request.data.get('name')

        if Category.objects.filter(name=name).exists():
            return Response("name already exists",status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':f"str(e)"},status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        limit=int(request.GET.get('limit'))
        offset=int(request.GET.get('offset'))

        queryset = Category.objects.all()
        queryset = queryset[offset:limit+offset]
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        category_id = UUID(request.GET.get('id'))

        if not category_id:
            return Response({"error": "id query parameter is required"},status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(id=category_id)
        except Exception as e:
            return Response({"error": "Category not found"},status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        category_id = UUID(request.GET.get('id'))
        name = request.data.get('name')
        description = request.data.get('description')

        category = Category.objects.get(id=category_id)
        category.name = name
        category.description = description

        serializer = CategorySerializer(category,data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f"str(e)"}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        category_id = UUID(request.GET.get('id'))
        category = Category.objects.get(id=category_id)

        if Category.objects.filter(name=request.data.get('name')).exclude(id=category_id).exists():
            return Response("name already exists",status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(category,data=request.data,partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error':f"str(e)"},status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        category_id = UUID(request.GET.get('id'))

        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return Response("Category deleted",status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error':f"{str(e)}"},status=status.HTTP_400_BAD_REQUEST)

    def all_category_delete(self, request, *args, **kwargs):
        Category.objects.all().delete()
        return Response("All Category deleted",status=status.HTTP_204_NO_CONTENT)








