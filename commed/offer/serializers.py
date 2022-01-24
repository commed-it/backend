from rest_framework import serializers
import base64, uuid
from django.core.files.base import ContentFile
from enterprise.serializers import EnterpriseSerializer
from product.serializers import ProductSerializer
from .models import Encounter, FormalOffer
from enterprise.serializers import EnterpriseSerializer
from product.serializers import ProductSerializer


class Base64Pdf(serializers.FileField):

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:application/pdf'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name=id.urn[9:] + '.' + ext)
        return super(Base64Pdf, self).to_internal_value(data)


class EncounterSerializer(serializers.ModelSerializer):
    """
    client = EnterpriseSerializer()
    product = ProductSerializer()
    """

    class Meta:
        model = Encounter
        fields = ('id', 'client', 'product')


class CreateIfNotExistsSerializer(serializers.Serializer):
    product = ProductSerializer()
    encounter = EncounterSerializer()
    enterprise = EnterpriseSerializer()


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
    version = serializers.IntegerField(required=False)
    pdf = Base64Pdf()

    class Meta:
        model = FormalOffer
        fields = ('encounterId', 'contract', 'pdf', 'state', 'version')

    def create(self, validated_data):
        try:
            last_fo = FormalOffer.objects.filter(encounterId=validated_data["encounterId"]).last()
            validated_data['version'] = last_fo.version + 1
            return FormalOffer.objects.create(**validated_data)
        except FormalOffer.DoesNotExist:
            validated_data['version'] = 0
            return FormalOffer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.pk = None
        instance.version += 1
        if validated_data['version']:
            del validated_data['version']
        for k, v in validated_data.items():
            instance.__setattr__(k, v)
        instance.save()
        return instance


class ListChatSerializer(serializers.Serializer):
    encounter = EncounterSerializer()
    product = ProductSerializer()
    theOtherClient = EnterpriseSerializer()


class FormalOfferEncounterSerializer(serializers.Serializer):
    encounter = EncounterSerializer()
    formalOffer = FormalOfferSerializer()
    product = ProductSerializer()
    theOtherClient = EnterpriseSerializer()


class FormalOfferEncounterSerializerFull(serializers.Serializer):
    encounter = EncounterSerializer()
    formalOffer = FormalOfferSerializer()
    product = ProductSerializer()
    client = EnterpriseSerializer()
    owner = EnterpriseSerializer()
