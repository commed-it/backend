import json
from django.forms import IntegerField
from rest_framework import serializers
import base64, uuid
from django.core.files.base import ContentFile
from chat.models import Message
from enterprise.serializers import EnterpriseSerializer
from product.serializers import ProductSerializer
from .models import Encounter, FormalOffer
from enterprise.serializers import EnterpriseSerializer
from product.serializers import ProductSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
        fields = '__all__'

    def create(self, validated_data):
        last_fo = FormalOffer.objects.filter(encounterId=validated_data["encounterId"]).last()
        if last_fo: 
            validated_data['version'] = last_fo.version + 1
        else:
            validated_data['version'] = 0
        fo = FormalOffer.objects.create(**validated_data)
        user = fo.encounterId.product.owner
        channel_layer = get_channel_layer()
        message = {
                'type': 'chat_message',
                'message': {
                    "user": user.id, 
                    "type": "formalOffer", 
                    "formalOffer": fo
                    }
                
            } 
        async_to_sync(channel_layer.group_send)(
            f"chat_{fo.encounterId}",
            message
        )
        new_msg = Message.objects.create(author=user.id,
                                         msg=json.dumps(message), channel_context=fo.encounterId)
        new_msg.save()
        return fo


    def update(self, instance, validated_data):
        instance.pk = None
        instance.version += 1
        if 'version' in validated_data.keys():
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

class SignSerializer(serializers.Serializer):
    fo = IntegerField()