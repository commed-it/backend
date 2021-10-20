from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "name", "product", "image")


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(source='productimage_set', many=True, required=False)

    class Meta:
        model = Product
        fields = ("id", "owner", "images", "description", "latitude", "longitude", "tag")
