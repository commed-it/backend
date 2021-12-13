from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .latlon import get_close_products
from .models import Product, ProductImage
from .nlp import search_by_tag
from .serializers import ProductSerializer, ProductImageSerializer, SearchRequestBodySerializer, RecomendationRequestBodySerializer


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

class RecomendationView(APIView):
    """
    RecomendationView for recommending the closest products to the user
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        result = []
        request = RecomendationRequestBodySerializer(data=request.data)
        request.is_valid(True)
        data = request.data
        products = list(get_close_products(data.pop('location')))
        if len(products) < 4:
            result = products
        else:
            result = products[:4]
        serializer = ProductSerializer(result, many=True)
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


#
# Create your views here.

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for interacting with Products
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [AllowAny]