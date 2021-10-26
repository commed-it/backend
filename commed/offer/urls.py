from rest_framework.routers import SimpleRouter
from .views import EncounterViewSet

router = SimpleRouter()
router.register("", EncounterViewSet)

urlpatterns = router.urls
