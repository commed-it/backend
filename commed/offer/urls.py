from rest_framework.routers import SimpleRouter
from .views import EncounterViewSet
from .views import FormalOfferViewSet

router = SimpleRouter()
router.register("encounter", EncounterViewSet)
router.register("formaloffer", FormalOfferViewSet)

urlpatterns = router.urls

