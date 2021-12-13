from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ProductViewSet, SearchView, UserProducts, RecomendationView, ProductImageViewSet

router = SimpleRouter()
router.register("", ProductViewSet)
router.register("images", ProductImageViewSet)

urlpatterns = [ path('search/', SearchView.as_view()),
                path('recomendation/', RecomendationView.as_view()),
                path('user/<int:user_id>', UserProducts.as_view()),
                ] + router.urls
