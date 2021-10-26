import datetime

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from ..models import Enterprise

# Create your tests here.
BASE_URL: str = "/enterprise/"


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

    def test_list_enterprise(self):
        """
        Test the list type in CRUD.
        """
        response = self.client.get(BASE_URL)
        self.assertEqual(200, response.status_code)

    def test_get_enterprise(self):
        """
        Test the get type in CRUD.
        """
        response = self.client.get(BASE_URL + "1/")
        self.assertEqual(200, response.status_code)

    def test_create_enterprise(self):
        """
        Test create enterprise
        """
        response = self.client.post(
            BASE_URL,
            {
                "owner": 2,
                "NIF": "987654321X",
                "name": "Another Enterprise",
                "contactInfo": "SO CALL ME BABY",
                "description": "<p>What do you mean by that?</p>",
            },
        )
        self.assertEqual(201, response.status_code)

    def test_update_enterprise(self):
        response = self.client.put(
            BASE_URL + "1/",
            {
                "owner": 1,
                "NIF": "987654321X",
                "name": "Another Enterprise",
                "contactInfo": "SO CALL ME BABY",
                "description": "<p>What do you mean by that?</p>",
            },
        )
        self.assertEqual(200, response.status_code)

    def test_patch_enterprise(self):
        response = self.client.patch(
            BASE_URL + "1/",
            {
                "description": "<p>What do you mean by that?</p>",
            },
        )
        self.assertEqual(200, response.status_code)

    def test_delete_enterprise(self):
        response = self.client.delete(BASE_URL + '1/')
        self.assertEqual(204, response.status_code)
