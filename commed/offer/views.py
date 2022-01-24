import os

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.core.mail import send_mail
from rest_framework.decorators import api_view

from .serializers import EncounterSerializer, FormalOfferSerializer, FormalOfferEncounterSerializer, ListChatSerializer, \
    TheOtherEncounterSerializer, CreateIfNotExistsSerializer, FormalOfferEncounterSerializerFull
from rest_framework import viewsets, generics
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


class FormalOfferFromFOViewSet(viewsets.GenericViewSet):
    serializer_class = FormalOfferSerializer
    permission_classes = [AllowAny]

    def list(self, *args, **kwargs):
        fo_id = kwargs['fo_id']
        fo = FormalOffer.objects.get(pk=fo_id)
        res = {
            'owner': Enterprise.objects.get(owner=fo.encounterId.product.owner),
            'encounter': fo.encounterId,
            'formalOffer': fo,
            'product': fo.encounterId.product,
            'client': Enterprise.objects.get(owner=fo.encounterId.client)
        }
        serializer = FormalOfferEncounterSerializerFull(res)
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


class CreateIfNotExistsEncounter(generics.CreateAPIView):
    serializer_class = EncounterSerializer
    queryset = Encounter.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            en = Encounter.objects.get(client=serializer.validated_data['client'],
                                       product=serializer.validated_data['product'])
            p1 = serializer.validated_data['product']
            data = {
                'product': p1,
                'encounter': en,
                'enterprise': Enterprise.objects.get(owner=p1.owner)
            }
            ser = CreateIfNotExistsSerializer(data)
            return Response(ser.data)
        except Encounter.DoesNotExist:
            v = serializer.save()
            p2 = serializer.validated_data['product']
            data = {
                'product': p2,
                'encounter': v,
                'enterprise': Enterprise.objects.get(owner=p2.owner)
            }
            ser = CreateIfNotExistsSerializer(data)
            return Response(ser.data)


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
    """Manteined for legacy reasons. """
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


@api_view(['POST'])
def send_confirmation_formal_offer_email(request, *args, **kwargs):
    """
    Sends an email with a confirmation for the formal offer.
    """
    if request.method == 'POST':
        user: User = request.user
        email = user.email
        send_mail(
            subject = '[ Commed ]: Confirmation of signing a formal offer',
            message = "",
            from_email = os.getenv('EMAIL_HOST_USER'),
            recipient_list = [email],
            html_message = """
            <html>
                <head>
                </head>
                <body>
                    <h1>This should contain a longer description</h1>
                    <p>This should be changed to have a button</p>
                <body>
            </html>
            """
        )
        return JsonResponse({'message': 'Email sent correctly'}, status=204)
    else:
        return JsonResponse({'message': 'method not allowed'}, status=405)

