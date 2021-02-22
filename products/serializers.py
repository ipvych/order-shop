from rest_framework import serializers, validators

from .models import ProductCategory, Product, ProductPicture

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPicture
        fields = ['picture']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    pictures = ProductPictureSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
