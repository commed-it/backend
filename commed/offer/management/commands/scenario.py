import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from chat.models import Message
from offer.models import Encounter, FormalOffer
from product.models import Product, Category, Tag, ProductImage
from enterprise.models import Enterprise
from unittest.mock import MagicMock
from django.core.files import File

class Command(BaseCommand):
    help = "Adds things to the database"

    def handle(self, *args, **kwargs):
        user_1 = User.objects.create_user(
            id=5,
            username="user5",
            password="complexpass",
            email="commed.usuari.prova@gmail.com",
            first_name="Anna",
            last_name="Riart",
        )
        Enterprise.objects.create(
            owner=user_1,
            NIF="2643671X",
            name="Restaurant l'Alpaca",
            contactInfo="alpaca@gmail.com",
            description="Restaurant l'Alpaca. També fem càterings per a esdeveniments.",
            profileImage="alpaca.png",
            bannerImage="alpacaBanner.jpg",
            location="Av. Pau Casals nº 8 de Cervera"
        )
