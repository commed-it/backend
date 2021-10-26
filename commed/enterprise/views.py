from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Enterprise
from .serializers import EnterpriseSerializer


#
# Create your views here.

class EnterpriseViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Enterprises
    """
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
    permission_classes = [AllowAny]
