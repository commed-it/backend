from django.shortcuts import render
from .serializers import EnterpriseSerializer
from .models import Enterprise
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
#
# Create your views here.

class EnterpriseViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Enterprises
    """
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
    permission_classes = [AllowAny]
