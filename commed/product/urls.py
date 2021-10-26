from rest_framework.routers import SimpleRouter

from .views import ProductViewSet

router = SimpleRouter()
router.register("", ProductViewSet)

urlpatterns = router.urls
