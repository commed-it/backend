from rest_framework.routers import SimpleRouter
from .views import EncounterViewSet
from .views import FormalOfferViewSet, UserFormalOffers, UserEncounter
from django.urls import path


router = SimpleRouter()
router.register("encounter", EncounterViewSet)
router.register("formaloffer", FormalOfferViewSet)

urlpatterns = [path('formaloffer/user/<int:user_id>', UserFormalOffers.as_view()),
               path('encounter/user/<int:user_id>', UserEncounter.as_view())] + router.urls

