from rest_framework.routers import SimpleRouter
from .views import EnterpriseViewSet

router = SimpleRouter()
router.register("", EnterpriseViewSet)

urlpatterns = router.urls
