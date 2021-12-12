
from enterprise.models import Enterprise
from .serializers import EncounterSerializer, FormalOfferSerializer, FormalOfferEncounterSerializer
from rest_framework import viewsets, mixins
from .models import FormalOffer
from rest_framework.permissions import AllowAny
from .models import Encounter
from rest_framework.views import APIView
from rest_framework.response import Response
from product.models import Product
import dataclasses as dto


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


@dto.dataclass
class FormalOFferFromUserDTO:
    formalOffer: dict
    encounter: dict
    product: dict
    theOtherClient: dict


def get_when_im_product_owner(user_id):
    im_the_product_owner = FormalOffer.objects.filter(encounterId__product__owner__id=user_id)
    list_po = list(im_the_product_owner.select_related('encounterId', 'encounterId__client', 'encounterId__product'))
    return ({
        'formalOffer': x,
        'encounter': x.encounterId,
        'product': x.encounterId.product,
        'theOtherClient': Enterprise.objects.get(owner=x.encounterId.client_id)
    } for x in list_po)


def get_when_im_client(user_id):
    imTheClient = FormalOffer.objects.filter(encounterId__client__id=user_id)
    listClient = list(
        imTheClient.select_related('encounterId', 'encounterId__product__owner', 'encounterId__product'))
    return ({
        'formalOffer': x,
        'encounter': x.encounterId,
        'product': x.encounterId.product,
        'theOtherClient': Enterprise.objects.get(owner=x.encounterId.product.owner_id)

    } for x in listClient)


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
