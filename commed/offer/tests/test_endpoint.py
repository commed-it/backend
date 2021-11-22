from django.db.models.fields.files import FileField
from django.test.client import Client
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from offer.models import Encounter, FormalOffer
from product.models import Product
from unittest.mock import MagicMock
from django.core.files import File
import json

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
        Sets Up the offer
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

    """

    ---------------------ENCOUNTER-------------------------
    
    """

    def test_list_encounter(self):
        """
        Test the list type in CRUD.
        """
        response = self.client.get(BASE_URL+"encounter/")
        self.assertEqual(200, response.status_code)

    def test_get_encounter(self):
        """
        Test the get type in CRUD.
        """
        response = self.client.get(BASE_URL + "encounter/" + "1/")
        self.assertEqual(200, response.status_code)

    def test_create_encounter(self):
        """
        Test create encounter
        """
        response = self.client.post(
            BASE_URL + "encounter/",
            {
                "client": 1,
                "product": 1

            },
        )
        self.assertEqual(201, response.status_code)

    def test_update_encounter(self):
        response = self.client.put(
            BASE_URL + "encounter/" + "1/",
            {
                "client": 1,
                "product": 1
            },
        )
        self.assertEqual(200, response.status_code)

    def test_patch_encounter(self):
        response = self.client.patch(
            BASE_URL + "encounter/" + "1/",
            {
                "client": 1,
            },
        )
        self.assertEqual(200, response.status_code)

    def test_delete_encounter(self):
        response = self.client.delete(BASE_URL + "encounter/" + '1/')
        self.assertEqual(204, response.status_code)

    """

    ---------------------FORMAL OFFER-------------------------
    
    """

    def test_list_formal_offer(self):
        """
        Test the list type in CRUD.
        """
        response = self.client.get(BASE_URL + "formaloffer/")
        self.assertEqual(200, response.status_code)

    def test_get_formal_offer(self):
        """
        Test the get type in CRUD.
        """
        response = self.client.get(BASE_URL + "formaloffer/" + "1/")
        self.assertEqual(200, response.status_code)

    def test_create_formal_offer(self):
        """
        Test create encounter
        """
        encounter = Encounter.objects.get(id=1)
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        response = self.client.post(
            BASE_URL + "formaloffer/",
            {
                "encounterId": encounter.id,
                "version": 1,
                "contract": "asdfasdfasdf",
                "signedPdf": file_mock
            },
        )
        self.assertEqual(201, response.status_code)

    def test_update_formal_offer(self):
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        encounter = Encounter.objects.get(id=1)
        response = self.client.put(
            BASE_URL + "formaloffer/" + "1/",
            {
                "encounterId": encounter.id,
                "version": 4,
                "contract": "hotal",
                "signedPdf": file_mock
            },
        )
        self.assertEqual(200, response.status_code)

    def test_patch_formal_offer(self):
        response = self.client.patch(
            BASE_URL + "formaloffer/" + "1/",
            {
                "contract": "adeu",
            },
        )
        self.assertEqual(200, response.status_code)

    def test_delete_formal_offer(self):
        response = self.client.delete(BASE_URL + "formaloffer/" + '1/')
        self.assertEqual(204, response.status_code)

    def test_list_user_formal_offer(self):
        """
        Test the list type in CRUD.
        """
        response = self.client.get(BASE_URL + "formaloffer/user/1")
        self.assertEqual(200, response.status_code)