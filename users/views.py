from uuid import UUID

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import *
from .serializers import UsersSerializer


# Create your views here.
class UsersViewSet(viewsets.ModelViewSet):
    queryset=Users.objects.all()
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        if Users.objects.filter(email=request.data.get('email')).exists():
            return Response({'message':'email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(phonenumber=request.data.get('phonenumber')).exists():
            return Response({'message':'phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UsersSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request, *args, **kwargs):
        queryset = Users.objects.all()
        serializer = UsersSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_id=UUID(request.GET.get('id'))
        user= Users.objects.get(id=user_id)
        email=request.data.get('email')
        phonenumber=request.data.get('phonenumber')

        if Users.objects.filter(email=email).exclude(id=user_id).exists():
            return Response({'message':'email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(phonenumber=phonenumber).exclude(id=user_id).exists():
            return Response({'message':'phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UsersSerializer(user,data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        user_id=UUID(request.GET.get('id'))
        user= Users.objects.get(id=user_id)
        serializer = UsersSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        user_id=UUID(request.GET.get('id'))
        user_id = UUID(request.GET.get('id'))
        user = Users.objects.get(id=user_id)
        email = request.data.get('email')
        phonenumber = request.data.get('phonenumber')

        if Users.objects.filter(email=email).exclude(id=user_id).exists():
            return Response({'message': 'email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(phonenumber=phonenumber).exclude(id=user_id).exists():
            return Response({'message': 'phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UsersSerializer(user, data=request.data,partial=True)
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user_id=UUID(request.GET.get('id'))
        user= Users.objects.get(id=user_id)
        try:
            user.delete()
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def all_delete_users(self, request, *args, **kwargs):
        Users.objects.all().delete()
        return Response({'message':'all deleted users'}, status=status.HTTP_200_OK)







