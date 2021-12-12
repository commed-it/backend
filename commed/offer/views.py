from django.shortcuts import render
from .serializers import EncounterSerializer, FormalOfferSerializer
from rest_framework import viewsets
from .models import FormalOffer
from rest_framework.permissions import AllowAny
from .models import Encounter
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product
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
        serializer = EncounterSerializer(response, many=True)
        return Response(serializer.data)