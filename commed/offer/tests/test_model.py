import datetime

from unittest.mock import MagicMock
from django.core.files import File
from django.test import TestCase
from django.contrib.auth.models import User
from offer.models import Encounter, FormalOffer
from product.models import Product
from django.core.files.uploadedfile import SimpleUploadedFile


class EncounterTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Sets Up the Grade
        """
        """
        Sets Up the Enterprises
        """

        user = User.objects.create(
            username="furnusmicrowavus",
            password="complexpass",
            email="furnace@gmail.com",
            first_name="Linguini",
            last_name="Kitchen",
        )

        product = Product.objects.create(
            owner=user,
            description="ekjpoeasjdmpa",
            latitude=0.0,
            longitude=0.0
        )
        client = User.objects.create(
            username="eminaa",
            password="complexpass",
            email="furnace@gmail.com",
            first_name="Linguini",
            last_name="Kitchen",
        )

        e = Encounter.objects.create(
            client=client,
            product=product
        )
        cls.encounter_uuid = e.id
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        FormalOffer.objects.create(
            encounterId=e,
            version=2,
            contract="asdfasdf",
            signedPdf=file_mock
        )

    def test_content(self):
        """
        Test content of encounter.
        """
        encounter = Encounter.objects.get(id=self.encounter_uuid)
        self.assertEqual(2, encounter.client.pk)
        self.assertEqual(1, encounter.product.pk)
        formal_offer = FormalOffer.objects.get(id=1)
        self.assertEqual(2, formal_offer.version)
        self.assertEqual("asdfasdf", formal_offer.contract)
        self.assertIn("test", formal_offer.signedPdf.name)
