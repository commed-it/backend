import os

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .serializers import EncounterSerializer, FormalOfferSerializer, FormalOfferEncounterSerializer, ListChatSerializer, \
    TheOtherEncounterSerializer, CreateIfNotExistsSerializer, FormalOfferEncounterSerializerFull, SignSerializer
from rest_framework import viewsets, generics
from .models import FormalOffer
from rest_framework.permissions import AllowAny
from .models import Encounter
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product
import dataclasses as dto
from enterprise.models import Enterprise
from commed.settings import ALLOWED_HOSTS

SIGN_TEMPLATE = 'sign-catalan.html'


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


class StartSignatureView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Sends an email with a confirmation for the formal offer.
        """
        user: User = self.request.user
        origin = self.request.headers['Origin']
        formaloffer : FormalOffer = FormalOffer.objects.get(pk=request.data["fo"])
        enterprise: Enterprise = Enterprise.objects.get(owner = formaloffer.encounterId.product.owner) 
        email = user.email
        port = ':443' if os.getenv("PORT")  else (':' + os.getenv("OPEN_PORT"))
        context = {
                "img" : ALLOWED_HOSTS[3] + port + enterprise.profileImage.url,
                "enterprise": enterprise.name,
                "product": formaloffer.encounterId.product.title,
                "sign": origin + "/signature/" + str(request.data["fo"]),
                "email": formaloffer.encounterId.product.owner.email,
            }
        message = render_to_string(SIGN_TEMPLATE, context)
        send_mail(
            subject = '[ Commed ]: Formal Offer Signature - '+ enterprise.name+' - '+ formaloffer.encounterId.product.title,
            message = "",
            from_email = os.getenv('EMAIL_HOST_USER'),
            recipient_list = [email],
            html_message = message
        )
        return JsonResponse({'message': 'Email sent correctly'}, status=204)

class ConfirmSignatureView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        fo = request.path.split('/')[-1]
        formal_offer = FormalOffer.objects.get
