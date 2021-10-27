import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from offer.models import Encounter
from product.models import Product


class EncounterTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Sets Up the Grade
        """
        """
        Sets Up the Enterprises
        """
        time = datetime.datetime(
            2020, 12, 13, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(0))
        )
        user_1 = User.objects.create(
            username="furnusmicrowavus",
            password="complexpass",
            email="furnace@gmail.com",
            first_name="Linguini",
            last_name="Kitchen",
        )
        user_2 = User.objects.create(
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
            username="eminaa",
            password="complexpass",
            email="furnace@gmail.com",
            first_name="Linguini",
            last_name="Kitchen",
        )
        client2 = User.objects.create(
            username="sergi",
            password="complexpass",
            email="quimpm@gmail.com",
            first_name="Macarroni",
            last_name="Diabola",
        )
        e = Encounter.objects.create(
            client=client1,
            product=product2
        )
        Encounter.objects.create(
            client=client2,
            product=product2
        )

    def test_content(self):
        encounter = Encounter.objects.get(id=1)
        self.assertEqual(3, encounter.client.pk)
        self.assertEqual(2, encounter.product.pk)
