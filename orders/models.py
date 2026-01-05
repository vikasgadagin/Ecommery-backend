import uuid

from django.db import models

from products.models import Products
from users.models import Users


# Create your models here.

class Orders(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(Users,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    address= models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now_add=True,editable=False)
    updated_at=models.DateTimeField(auto_now=True,editable=False)

    class Meta:
        db_table = 'orders'
