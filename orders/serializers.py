from rest_framework.serializers import ModelSerializer
from orders.models import Orders
from products.models import Products
from products.serializers import ProductsSerializer
from users.models import Users
from users.serializers import *

class OrderSerializer(serializers.ModelSerializer):
       class Meta:
           model = Orders
           fields = '__all__'

class OrderListSerializer(serializers.ModelSerializer):
    userFields=serializers.SerializerMethodField()
    productFields=serializers.SerializerMethodField()

    def get_userFields(self,obj):
        return UsersSerializer(obj.user).data

    def get_productFields(self,obj):
        return ProductsSerializer(obj.product).data

    class Meta:
        model = Orders
        fields = '__all__'







