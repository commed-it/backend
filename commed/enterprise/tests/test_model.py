import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import MagicMock
from django.core.files.images import ImageFile


from ..models import Enterprise


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
        profile_image = MagicMock(spec=ImageFile)
        profile_image.name = 'ProfileImage.jpg'
        banner_image = MagicMock(spec=ImageFile)
        banner_image.name = 'BannerImage.jpg'
        Enterprise.objects.create(
            owner=user_1,
            NIF="12345678X",
            name="Restaurant Paco",
            contactInfo="paco@paco.com",
            description="<strong>This is a strong statement, lady</strong>",
            profileImage=profile_image,
            bannerImage=banner_image
        )
        Enterprise.objects.create(
            owner=user_2,
            NIF="21345678X",
            name="Restaurant PaNco",
            contactInfo="paco@paco.com",
            description="<strong>This is a strong statement, lady</strong>",
            profileImage=profile_image,
            bannerImage=banner_image
        )

    def test_content(self):
        enterprise = Enterprise.objects.get(id=1)
        self.assertEqual(1, enterprise.owner.pk)
        self.assertEqual('12345678X', enterprise.NIF)

