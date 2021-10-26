from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Product
from .serializers import ProductSerializer


#
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Enterprises
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
