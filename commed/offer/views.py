from .serializers import EncounterSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Encounter


class EncounterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Enterprises
    """
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer
    permission_classes = [AllowAny]
