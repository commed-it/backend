from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny

from .models import Enterprise
from .serializers import EnterpriseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


#
# Create your views here.

class EnterpriseViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Enterprises
    """
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
    permission_classes = [AllowAny]

class UserEnterprise(APIView):

    def get(self, request, *args, **kwargs):
        user = request.path.split('/')[-1]
        enterprise = Enterprise.objects.get(owner=user)
        serializer = EnterpriseSerializer(enterprise)
        return Response(serializer.data)
