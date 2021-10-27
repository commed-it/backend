from django.shortcuts import render
from .serializers import EncounterSerializer
from rest_framework import viewsets
from .serializers import FormalOfferSerializer
from .models import FormalOffer
from rest_framework.permissions import AllowAny
from .models import Encounter


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

