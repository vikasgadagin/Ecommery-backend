from uuid import UUID

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from category import serializers
from products.serializers import *
from products.models import Products


# Create your views here.



class ProductViewSet(viewsets.ModelViewSet):
    queryset=Products.objects.all()
    serializer_class=ProductsSerializer

    def create(self,request,*args,**kwargs):
        if Products.objects.filter(name=request.data['name']).exists():
            return Response({'message':"product areadly exists"},status=status.HTTP_400_BAD_REQUEST)
        serializer=ProductsSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.all()
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def retrieve(self,request,pk):
        product_id=UUID(request.data.get('id'))
        product=Products.objects.get(id=product_id)

        serializer = ProductsSerializer(product)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        product_id=UUID(request.GET.get('id'))
        product=Products.objects.get(id=product_id)
        if Products.objects.filter(name=request.data.get('name')).exclude(id=product_id).exists():
            return Response({'message': "product areadly exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductsSerializer(product,data=request.data,partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        product_id=UUID(request.GET.get('id'))
        product=Products.objects.get(id=product_id)
        if Products.objects.filter(name=request.data.get('name')).exclude(id=product_id).exists():
            return Response({'message': "product areadly exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductsSerializer(product, data=request.data, partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        product_id=UUID(request.GET.get('id'))
        product=Products.objects.get(id=product_id)
        try:
            product.delete()
            return Response({'message': "product deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)














