from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import CustomUserSerializer


# Create your views here.


class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

