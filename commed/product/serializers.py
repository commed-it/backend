from rest_framework import serializers

from .models import Product, ProductImage, Tag, Category
from .utils import category_similarity


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "name", "image")


def check_categories(validated_data):
    tag_name = validated_data['name']
    try:
        instance = Tag.objects.get(name=tag_name)
        return instance
    except:
        pass
    cats = category_similarity(tag_name)
    instance_tag = Tag.objects.create(name=tag_name)
    if len(cats) == 0:
        instance_cat = Category.objects.create(name=tag_name)
        instance_cat.tag_children.set([instance_tag])
    else:
        for cat in cats.keys():
            cat.tag_children.add(instance_tag)
    return instance_tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

    def create(self, validaded_data):
        instance = check_categories(validaded_data)
        return instance


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(source='productimage_set', many=True, required=False)
    tag = TagSerializer(read_only=False, many=True)

    class Meta:
        model = Product
        fields = ("id", "owner", "images", "description", "latitude", "longitude", "tag")

    def create(self, validated_data):
        tags = [check_categories(tag) for tag in validated_data.pop('tag')]
        productimages = validated_data.pop('productimage_set')
        instance = Product.objects.create(**validated_data)
        for image in productimages:
            image['product'] = instance
            ProductImage.objects.create(**image)
        instance.tag.set(tags)
        return instance
