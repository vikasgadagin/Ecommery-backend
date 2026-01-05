from rest_framework.serializers import ModelSerializer

from category.models import Category
from .models import *
from category.serializers import *

class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    categoryFields = serializers.SerializerMethodField()

    def get_categoryFields(self, obj):
        return CategorySerializer(obj.category).data

    class Meta:
        model = Products
        fields = '__all__'

