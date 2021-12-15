from rest_framework import serializers

from .models import Enterprise
from product.serializers import Base64ImageField


class EnterpriseSerializer(serializers.ModelSerializer):
    profileImage = Base64ImageField(read_only = False, required=False)
    bannerImage = Base64ImageField(read_only = False, required=False)
    location = serializers.CharField(required=False)

    class Meta:
        model = Enterprise
        fields = ("id", "owner", "NIF", "name", "contactInfo", "description", "profileImage", "bannerImage", "location")
