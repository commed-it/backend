from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ProductViewSet, SearchView, UserProducts

router = SimpleRouter()
router.register("", ProductViewSet)

urlpatterns = [ path('search/', SearchView.as_view()),
                path('user/<int:user_id>', UserProducts.as_view()),
                ] + router.urls
