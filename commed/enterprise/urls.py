from rest_framework.routers import SimpleRouter
from django.urls import path

from .views import EnterpriseViewSet, UserEnterprise

router = SimpleRouter()
router.register("", EnterpriseViewSet)

urlpatterns = [path('user/<int:user_id>', UserEnterprise.as_view())] + router.urls
