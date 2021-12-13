from rest_framework import serializers

from enterprise.serializers import EnterpriseSerializer
from product.serializers import ProductSerializer
from .models import Encounter, FormalOffer
from enterprise.serializers import EnterpriseSerializer
from product.serializers import ProductSerializer


class EncounterSerializer(serializers.ModelSerializer):
    """
    client = EnterpriseSerializer()
    product = ProductSerializer()
    """

    class Meta:
        model = Encounter
        fields = ('id', 'client', 'product')


class TheOtherEncounterSerializer(serializers.ModelSerializer):
    """
    client = EnterpriseSerializer()
    product = ProductSerializer()
    """
    client = EnterpriseSerializer()
    product = ProductSerializer()

    class Meta:
        model = Encounter
        fields = ('id', 'client', 'product')


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
