from django.shortcuts import render
from .serializers import EncounterSerializer, FormalOfferSerializer, FormalOfferEncounterSerializer, ListChatSerializer, \
    TheOtherEncounterSerializer
from rest_framework import viewsets
from .models import FormalOffer
from rest_framework.permissions import AllowAny
from .models import Encounter
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product
import dataclasses as dto
from enterprise.models import Enterprise


class EncounterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Enterprises
    """
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer
    permission_classes = [AllowAny]


class FormalOfferViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Enterprises
    """
    queryset = FormalOffer.objects.all()
    serializer_class = FormalOfferSerializer
    permission_classes = [AllowAny]


def get_when_im_product_owner(user_id):
    im_the_product_owner = FormalOffer.objects.filter(encounterId__product__owner__id=user_id)
    list_po = list(im_the_product_owner.select_related('encounterId', 'encounterId__client', 'encounterId__product'))
    return ({
        'formalOffer': x,
        'encounter': x.encounterId,
        'product': x.encounterId.product,
        'theOtherClient': Enterprise.objects.get(owner=x.encounterId.client)
    } for x in list_po)


def get_when_im_client(user_id):
    imTheClient = FormalOffer.objects.filter(encounterId__client__id=user_id)
    listClient = list(
        imTheClient.select_related('encounterId', 'encounterId__product__owner', 'encounterId__product'))
    return ({
        'formalOffer': x,
        'encounter': x.encounterId,
        'product': x.encounterId.product,
        'theOtherClient': Enterprise.objects.get(owner=x.encounterId.product.owner)

    } for x in listClient)


def get_when_im_product_owner_encounter(user_id):
    im_the_product_owner = Encounter.objects.filter(product__owner__id=user_id)
    list_po = list(im_the_product_owner.select_related('client', 'product'))
    return ({
        'encounter': x,
        'product': x.product,
        'theOtherClient': Enterprise.objects.get(owner=x.client)
    } for x in list_po)


def get_when_im_client_encounter(user_id):
    im_the_client = Encounter.objects.filter(client__id=user_id)
    list_client = list(
        im_the_client.select_related('product__owner', 'product'))
    return ({
        'encounter': x,
        'product': x.product,
        'theOtherClient': Enterprise.objects.get(owner=x.product.owner)

    } for x in list_client)


class FormalOfferFromUserViewSet(viewsets.GenericViewSet):
    serializer_class = FormalOfferSerializer
    permission_classes = [AllowAny]

    def list(self, *args, **kwargs):
        user_id = kwargs['user_id']
        res = []
        res.extend(get_when_im_client(user_id))
        res.extend(get_when_im_product_owner(user_id))
        serializer = FormalOfferEncounterSerializer(res, many=True)
        return Response(serializer.data)


class ListChatsViewSet(viewsets.GenericViewSet):
    serializer_class = FormalOfferSerializer
    permission_classes = [AllowAny]

    def list(self, *args, **kwargs):
        user_id = kwargs['user_id']
        res = []
        res.extend(get_when_im_client_encounter(user_id))
        res.extend(get_when_im_product_owner_encounter(user_id))
        serializer = ListChatSerializer(res, many=True)
        return Response(serializer.data)


class CreateIfNotExistsEncounter(viewsets.GenericViewSet):
    serializer_class = EncounterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """ha"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            en = Encounter.objects.get(client=serializer.validated_data['client'],
                                       product=serializer.validated_data['product'])
            ser = self.get_serializer(en)
            return Response(ser.data)
        except Encounter.DoesNotExist:
            v = serializer.save()
            return Response(serializer.data)


class UserFormalOffers(APIView):
    """
    Get all the Products owned by a user
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        encounters = []
        formal_offers = []
        user = request.path.split('/')[-1]
        products = list(Product.objects.filter(owner=user))
        for product in products:
            encounters = encounters + list(Encounter.objects.filter(product=product.id))
        for encounter in encounters:
            formal_offers.append(FormalOffer.objects.get(encounterId=encounter))
        serializer = FormalOfferSerializer(formal_offers, many=True)
        return Response(serializer.data)


class UserEncounter(APIView):
    """Get some"""
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        encounters = []
        response = []
        user = request.path.split('/')[-1]
        products = list(Product.objects.filter(owner=user))
        for product in products:
            encounters = encounters + list(Encounter.objects.filter(product=product.id))
            for encounter in encounters:
                client = Enterprise.objects.get(owner=encounter.client)
                response.append({
                    "id": encounter.id,
                    "product": product,
                    "client": client
                })
        encounters_client = Encounter.objects.filter(client=user)
        client = Enterprise.objects.get(owner=user);
        for encounter in encounters_client:
            response.append({
                "id": encounter.id,
                "product": encounter.product,
                "client": client
            })
        serializer = TheOtherEncounterSerializer(response, many=True)
        return Response(serializer.data)
