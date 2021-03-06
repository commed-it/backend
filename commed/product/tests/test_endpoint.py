import datetime
import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from ..models import Product, Tag

# Create your tests here.
BASE_URL: str = "/product/"


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
        self.fruit = Tag.objects.create(
            name="fruit"
        )
        p = Product.objects.create(
            owner=user_2,
            description="gertgtg3",
            latitude=0.0,
            longitude=0.0
        )
        Product.objects.create(
            owner=user_1,
            description="ekjpoeasjdmpa",
            latitude=0.0,
            longitude=0.0
        )

    def test_list_product(self):
        """
        Test the list type in CRUD.
        """
        response = self.client.get(BASE_URL)
        self.assertEqual(200, response.status_code)

    def test_get_product(self):
        """
        Test the get type in CRUD.
        """
        response = self.client.get(BASE_URL + "1/")
        self.assertEqual(200, response.status_code)

    def test_create_product(self):
        """
        Test create enterprise
        """
        fruit_ = json.dumps({
            "owner": 1,
            "title": "A title for create product",
            "description": "ekjpoeasjdmpa",
            "tag": [{"name": "fruit"}],
            "latitude": 0.0,
            "longitude": 0.0,
        })
        response = self.client.post(
            BASE_URL,
            fruit_, content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

    def test_update_product(self):
        response = self.client.put(
            BASE_URL + "1/",
            json.dumps({
                "owner": 1,
                "title": "Title for update",
                "description": "ekjpoeasjdmpa",
                "latitude": 0.0,
                "longitude": 0.0,
                "tag": [{"name":"fruit"}],
                "images": [],
            }), content_type='application/json'
        )
        self.assertEqual(200, response.status_code)

    def test_patch_product(self):
        response = self.client.patch(
            BASE_URL + "1/",
            {
                "description": "<p>What do you mean by that?</p>",
            },
        )
        self.assertEqual(200, response.status_code)

    def test_delete_product(self):
        response = self.client.delete(BASE_URL + '1/')
        self.assertEqual(204, response.status_code)

    def test_list_product(self):
        """
        Test the list type in CRUD.
        """
        response = self.client.get(BASE_URL+"user/1")
        self.assertEqual(200, response.status_code)

