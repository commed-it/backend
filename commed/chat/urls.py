from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("messages", views.MessageViewSet, basename="messages")

urlpatterns = [path('<str:room_name>/', views.room, name='room'),
               path('encounter/<str:encounter_uuid>/', include(router.urls), name='messages'),
               ]
