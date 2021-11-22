from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .latlon import get_close_products
from .models import Product, ProductImage
from .nlp import search_by_tag
from .serializers import ProductSerializer, SearchRequestBodySerializer


#
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class SearchView(APIView):
    """
    SearchView for searching Products by tags and localization
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        request = SearchRequestBodySerializer(data=request.data)
        request.is_valid(True)
        data = request.data
        products = get_close_products(data.pop('location'))
        if data.__contains__('tags'):
            products = search_by_tag(products, data)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class UserProducts(APIView):
    """
    Get all the Products owned by a user
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = request.path.split('/')[-1]
        products = Product.objects.filter(owner=user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

