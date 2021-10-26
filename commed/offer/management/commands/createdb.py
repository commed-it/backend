import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from offer.models import Encounter, FormalOffer
from product.models import Product
from unittest.mock import MagicMock
from django.core.files import File

class Command(BaseCommand):
    help = "Adds things to the database"

    def handle(self, *args, **kwargs):
        user_1 = User.objects.create(
            id=-1,
            username="furnusmicrowavus",
            password="complexpass",
            email="furnace@gmail.com",
            first_name="Linguini",
            last_name="Kitchen",
        )
        user_2 = User.objects.create(
            id=-2,
            username="quimpm",
            password="complexpass",
            email="quimpm@gmail.com",
            first_name="Macarroni",
            last_name="Diabola",
        )

        product1 = Product.objects.create(
            owner=user_2,
            description="gertgtg3",
            latitude=0.0,
            longitude=0.0
        )
        product2 = Product.objects.create(
            owner=user_1,
            description="ekjpoeasjdmpa",
            latitude=0.0,
            longitude=0.0
        )
        client1 = User.objects.create(
            username="emina",
            password="complexpass",
            email="furnace@gmail.com",
            first_name="Linguini",
            last_name="Kitchen",
        )
        client2 = User.objects.create(
            username="nico",
            password="complexpass",
            email="quimpm@gmail.com",
            first_name="Macarroni",
            last_name="Diabola",
        )
        e = Encounter.objects.create(
            client=client1,
            product=product1
        )
        e2 = Encounter.objects.create(
            client=client2,
            product=product2
        )
        
        # FormalOffer
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        FormalOffer.objects.create(
            encounterId = e,
            version = 2,
            contract = "adsfasdf",
            signedPdf = file_mock
        )
        FormalOffer.objects.create(
            encounterId = e2,
            version = 3,
            contract = "adsfasdf",
            signedPdf = file_mock
        )

