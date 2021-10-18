from django.urls import path
from .views import UserRetrieve

urlpatterns = [path("<int:pk>/", UserRetrieve.as_view())]
