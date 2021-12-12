from rest_framework import serializers

from .models import Encounter, FormalOffer
from enterprise.serializers import EnterpriseSerializer
from product.serializers import ProductSerializer


class EncounterSerializer(serializers.ModelSerializer):
    client = EnterpriseSerializer()
    product = ProductSerializer()

    class Meta:
        model = Encounter
        fields = ("id", "client", "product")


class FormalOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormalOffer
        fields = ("encounterId", "version", "contract", "signedPdf")
