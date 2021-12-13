from rest_framework.routers import SimpleRouter
from .views import EncounterViewSet
from .views import FormalOfferViewSet, FormalOfferFromUserViewSet, ListChatsViewSet, CreateIfNotExistsEncounter
from django.urls import path

router = SimpleRouter()
router.register("encounter", EncounterViewSet)
router.register("formaloffer", FormalOfferViewSet)

urlpatterns = \
    [
        path('formaloffer/fromUser/<int:user_id>', FormalOfferFromUserViewSet.as_view({'get': 'list'})),
        path('encounter/fromUser/<int:user_id>', ListChatsViewSet.as_view({'get': 'list'})),
        path('encounter/create-if-not-exists/', CreateIfNotExistsEncounter.as_view({'post': 'create'})),
    ] + router.urls


