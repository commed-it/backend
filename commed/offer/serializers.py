from rest_framework import serializers

from enterprise.serializers import EnterpriseSerializer
from product.serializers import ProductSerializer
from .models import Encounter, FormalOffer


class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encounter
        fields = '__all__'


class FormalOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormalOffer
        fields = '__all__'


class ListChatSerializer(serializers.Serializer):
    encounter = EncounterSerializer()
    product = ProductSerializer()
    theOtherClient = EnterpriseSerializer()

class FormalOfferEncounterSerializer(serializers.Serializer):
    encounter = EncounterSerializer()
    formalOffer = FormalOfferSerializer()
    product = ProductSerializer()
    theOtherClient = EnterpriseSerializer()
