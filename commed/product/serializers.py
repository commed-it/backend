from rest_framework import serializers
import base64, uuid
from django.core.files.base import ContentFile

from .models import Product, ProductImage, Tag, Category
from .nlp import category_similarity

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,') # format ~= data:image/X,
            ext = format.split('/')[-1] # guess file extension
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name = id.urn[9:] + '.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)


class ProductImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
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
        fields = ("id", "owner", "title", "images", "description", "latitude", "longitude", "tag")


    def create(self, validated_data):
        tags = [check_categories(tag) for tag in validated_data.pop('tag')]
        productimages = []
        if validated_data.__contains__('productimage_set'):
            productimages = validated_data.pop('productimage_set')
        instance = Product.objects.create(**validated_data)
        for image in productimages:
            image['product'] = instance
            ProductImage.objects.create(**image)
        instance.tag.set(tags)
        return instance

    def update(self, instance, validated_data):
        print(instance)
        if validated_data.__contains__('tag'):
            tags = [check_categories(tag) for tag in validated_data.pop('tag')]
        productimages = []
        if validated_data.__contains__('productimage_set'):
            productimages = validated_data.pop('productimage_set')
        Product.objects.filter(pk=instance.pk).update(**validated_data)
        for image in productimages:
            image['product'] = instance
            ProductImage.objects.create(**image)
        instance.tag.set(tags)
        return instance


class LocationSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    distance_km = serializers.FloatField()


class SearchRequestBodySerializer(serializers.Serializer):
    tags = TagSerializer(many=True, required=False)
    location = LocationSerializer()

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Must include at least one field on request body")
        return data


class RecomendationRequestBodySerializer(serializers.Serializer):
    location = LocationSerializer()

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Must include at least one field on request body")
        return data

