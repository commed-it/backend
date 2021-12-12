import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from offer.models import Encounter, FormalOffer
from product.models import Product, Category, Tag, ProductImage
from enterprise.models import Enterprise
from unittest.mock import MagicMock
from django.core.files import File

class Command(BaseCommand):
    help = "Adds things to the database"

    def handle(self, *args, **kwargs):
        user_1 = User.objects.create(
            id=1,
            username="furnusmicrowavus",
            password="complexpass",
            email="furnace@gmail.com",
            first_name="Linguini",
            last_name="Kitchen",
        )
        user_2 = User.objects.create(
            id=2,
            username="quimpm",
            password="complexpass",
            email="quimpm@gmail.com",
            first_name="Macarroni",
            last_name="Diabola",
        )

        product1 = Product.objects.create(
            owner=user_2,
            description="Bananas",
            latitude=0.0,
            longitude=0.0
        )
        product2 = Product.objects.create(
            owner=user_1,
            description="Pineaples",
            latitude=0.0,
            longitude=0.0
        )
        apple_tag = Tag.objects.create(
            name="apple"
        )
        apples_tag = Tag.objects.create(
            name="apples"
        )
        pear_tag = Tag.objects.create(
            name="pear"
        )
        pears_tag = Tag.objects.create(
            name="pears"
        )
        dishwasher_tag = Tag.objects.create(
            name="dishwasher"
        )
        microwave_tag = Tag.objects.create(
            name="microwave"
        )
        cat_apple = Category.objects.create(
            name="apple",
        )
        cat_apple.tag_children.set([apple_tag, apples_tag, pear_tag, pears_tag])
        cat_dishwasher = Category.objects.create(
            name="dishwasher",
        )
        cat_dishwasher.tag_children.set([dishwasher_tag, microwave_tag])
        self.fruit = Product.objects.create(
            owner=user_2,
            title="Some fruit",
            description="gertgtg3",
            latitude=0.0,
            longitude=0.0,
        )
        self.fruit.tag.set([apple_tag, apples_tag, pear_tag, pears_tag])
        self.microwave = Product.objects.create(
            owner=user_1,
            title="Good Microwave",
            description="ekjpoeasjdmpa",
            latitude=2.0,
            longitude=3.0
        )
        self.microwave.tag.set([dishwasher_tag, microwave_tag])
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
            pdf = file_mock
        )
        FormalOffer.objects.create(
            encounterId = e2,
            version = 3,
            contract = "adsfasdf",
            pdf = file_mock
        )
        Enterprise.objects.create(
            owner=user_1,
            NIF="12345678X",
            name="Restaurant Paco",
            contactInfo="paco@paco.com",
            description="<strong>This is a strong statement, lady</strong>",
        )
        Enterprise.objects.create(
            owner=user_2,
            NIF="21345678X",
            name="Restaurant PaNco",
            contactInfo="paco@paco.com",
            description="<strong>This is a strong statement, lady</strong>",
        )
