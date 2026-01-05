import uuid

from django.db import models

# Create your models here.
class Users(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    phonenumber=models.CharField(max_length=10,unique=True)
    email=models.EmailField(unique=True)
    address=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True,editable=False)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='users'