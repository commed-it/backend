import datetime

from django.test import TestCase
from django.contrib.auth.models import User

from enterprise.models import Enterprise


class GradesTestCase(TestCase):

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


    def test_content(self):
        enterprise = Enterprise.objects.get(id=1)
        self.assertEqual(1, enterprise.owner.pk)
        self.assertEqual('12345678X', enterprise.NIF)
