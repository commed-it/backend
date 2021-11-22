import json

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase

from ..latlon import get_close_products
from ..models import Product, Tag, Category

# Create your tests here.
BASE_URL: str = "/product/search/"


class ApiCRUDWorks(APITestCase):
    pass


class MinMaxLatLonTest(TestCase):

    @classmethod
    def setUpTestData(self):
        """
        Sets Up the Products
        """
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
        self.FRUIT_DICT = {'id': 1, 'owner': 2, 'title': 'Some fruit', 'images': [], 'description': 'gertgtg3',
                           'latitude': 0.0,
                           'longitude': 0.0,
                           'tag': [{'name': 'apple'}, {'name': 'apples'}, {'name': 'pear'}, {'name': 'pears'}]}
        self.MICROWAVE_DICT = {'id': 2, 'owner': 1, 'title': 'Good Microwave', 'images': [],
                                'description': 'ekjpoeasjdmpa',
                                'latitude': 2.0, 'longitude': 3.0,
                                'tag': [{'name': 'dishwasher'}, {'name': 'microwave'}]}

    def test_content_lat_lon(self):
        products = get_close_products({"latitude": 0, "longitude": -1, "distance_km": 300})
        self.assertIn(self.fruit, products)
        self.assertNotIn(self.microwave, products)

    def test_content_lat_lon_and_tags_anyone(self):
        body = json.dumps({
            "tags": [
                {
                    "name": "dishwasher"
                }
            ],
            "location": {
                "longitude": 0.0,
                "latitude": -1,
                "distance_km": 300
            }
        })
        response = self.client.post(
            BASE_URL,
            body, content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        current = json.loads(response.content)
        self.assertTrue(len(current) == 0)

    def test_content_lat_lon_and_tags_fruit(self):
        body = json.dumps({
            "tags": [
                {
                    "name": "banana"
                }
            ],
            "location": {
                "longitude": 0.0,
                "latitude": -1,
                "distance_km": 300
            }
        })
        response = self.client.post(
            BASE_URL,
            body, content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        current = json.loads(response.content)
        expected = [self.FRUIT_DICT]
        self.assertEqual(expected, current)

    def test_content_lat_lon_and_tags_only_dishwasher(self):
        body = json.dumps({
            "tags": [
                {
                    "name": "microwave"
                }
            ],
            "location": {
                "longitude": 0.0,
                "latitude": -1,
                "distance_km": 30000
            }
        })
        response = self.client.post(
            BASE_URL,
            body, content_type='application/json'
        )
        self.assertEqual(200, response.status_code)
        current = json.loads(response.content)
        expected = [self.MICROWAVE_DICT]
        self.assertEqual(expected, current)
