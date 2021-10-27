import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from product.models import Product


class ProductTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Sets Up the Products
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
        p = Product.objects.create(
            owner=user_2,
            description="gertgtg3",
            latitude=0.0,
            longitude=0.0
        )
        p.tag.add()
        Product.objects.create(
            owner=user_1,
            description="ekjpoeasjdmpa",
            latitude=0.0,
            longitude=0.0
        )

    def test_content(self):
        product = Product.objects.get(id=1)
        self.assertEqual(2, product.owner.pk)
        self.assertEqual("gertgtg3", product.description)
