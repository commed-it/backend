from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from offer.models import Encounter
from product.models import Product
import datetime

# Create your tests here.
BASE_URL: str = "/offer/"


class ApiCRUDWorks(APITestCase):
    """
    This class serves as an API test for the CRUD operations.
    It will give a sense of a copy-pasting methodology for the other tests,
    as well as a structure to follow for CRUD apps.
    """

    @classmethod
    def setUp(self):
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
        Encounter.objects.create(
            client=client2,
            product=product2
        )

    def test_list_encounter(self):
        """
        Test the list type in CRUD.
        """
        response = self.client.get(BASE_URL)
        self.assertEqual(200, response.status_code)

    def test_get_encounter(self):
        """
        Test the get type in CRUD.
        """
        response = self.client.get(BASE_URL + "1/")
        self.assertEqual(200, response.status_code)

    def test_create_encounter(self):
        """
        Test create encounter
        """
        response = self.client.post(
            BASE_URL,
            {
                "client": 1,
                "product": 1

            },
        )
        self.assertEqual(201, response.status_code)

    def test_update_encounter(self):
        response = self.client.put(
            BASE_URL + "1/",
            {
                 "client": 1,
                "product": 1
            },
        )
        self.assertEqual(200, response.status_code)

    def test_patch_encounter(self):
        response = self.client.patch(
            BASE_URL + "1/",
            {
                "description": "<p>What do you mean by that?</p>",
            },
        )
        self.assertEqual(200, response.status_code)

    def test_delete_encounter(self):
        response = self.client.delete(BASE_URL + '1/')
        self.assertEqual(204, response.status_code)
