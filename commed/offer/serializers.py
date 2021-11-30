from rest_framework import serializers

from .models import Encounter, FormalOffer


class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = ("id", "client", "product")


class FormalOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormalOffer
        fields = ("encounterId", "version", "contract", "signedPdf")
