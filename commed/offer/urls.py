from rest_framework.routers import SimpleRouter
from .views import EncounterViewSet
from .views import FormalOfferViewSet, UserFormalOffers, FormalOfferFromUserViewSet, ListChatsViewSet
from django.urls import path

router = SimpleRouter()
router.register("encounter", EncounterViewSet)
router.register("formaloffer", FormalOfferViewSet)

urlpatterns = \
    [
        path('formaloffer/user/<int:user_id>', UserFormalOffers.as_view()),
        path('formaloffer/fromUser/<int:user_id>', FormalOfferFromUserViewSet.as_view({'get': 'list'})),
        path('encounter/fromUser/<int:user_id>', ListChatsViewSet.as_view({'get': 'list'})),
    ] + router.urls
