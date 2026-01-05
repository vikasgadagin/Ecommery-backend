from itertools import product
from uuid import UUID

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from orders.models import Orders
from orders.serializers import OrderSerializer
from products.models import Products
from products.serializers import ProductsSerializer
from users.models import Users
from .models import *

# Create your views here.
class OrdersViewSet(viewsets.ModelViewSet):
    queryset =Orders.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
         user_id=UUID(request.data.get('user'))
         product_id = UUID(request.data.get('product'))
         if not Users.objects.filter(id=user_id).exists():
             return Response({'message':'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
         if not Products.objects.filter(id=product_id).exists():
             return Response({'message':'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)
         product = Products.objects.get(id=product_id)
         if product.stock <= 0:
             return Response({'message': 'Product is out of stock'},status=status.HTTP_400_BAD_REQUEST)

             # Reduce stock
         product.stock = product.stock - 1
         product.save()
         serializer = OrderSerializer(data=request.data)
         try:
             if serializer.is_valid(raise_exception=True):
                 serializer.save()

                 return Response(serializer.data, status=status.HTTP_201_CREATED)
         except Exception as e:
             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)




    def update(self, request,pk=None, *args, **kwargs):

            # order_id = UUID(request.GET.get("order_id"))
            product_id = request.data.get("product")
            user_id = request.data.get("user")


            order = Orders.objects.get(id=pk)
            oldproduct = Products.objects.get(id=order.product.id)
            # user = Users.objects.get(id=order.user)


            temp1= oldproduct.stock
            temp2=  temp1+1
            oldproduct.stock= temp2
            oldproduct.save()

            newProduct = Products.objects.get(id=product_id)


            if newProduct.stock <= 0:
                return Response({"message": "Product out of stock"},status=status.HTTP_400_BAD_REQUEST)

            temp1=newProduct.stock
            temp2= temp1 -1
            newProduct.stock = temp2
            newProduct.save()


            order.product = newProduct
            serializer = OrderSerializer(order,data=request.data,partial=True)
            try:
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        order_id= request.GET.get('id')
        order_id = UUID(order_id)
        order = Orders.objects.get(id=order_id)
        serializer = OrderSerializer(order)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.delete()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


            order.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)


















