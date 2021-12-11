import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from offer.models import Encounter, FormalOffer
from product.models import Product, Category, Tag, ProductImage
from enterprise.models import Enterprise
from unittest.mock import MagicMock
from django.core.files import File
from media import images

class Command(BaseCommand):
    help = "Adds things to the database"

    def handle(self, *args, **kwargs):
        user_1 = User.objects.create(
            id=1,
            username="user1",
            password="complexpass",
            email="user1@gmail.com",
            first_name="John",
            last_name="Doe",
        )
        user_2 = User.objects.create(
            id=2,
            username="user2",
            password="complexpass",
            email="user2@gmail.com",
            first_name="Jane",
            last_name="Joe",
        )
        user_3 = User.objects.create(
            id=3,
            username="user3",
            password="complexpass",
            email="user3@gmail.com",
            first_name="Jamie",
            last_name="Oliver",
        )
        user_4 = User.objects.create(
            id=4,
            username="user4",
            password="complexpass",
            email="user4@gmail.com",
            first_name="Blues",
            last_name="Crews",
        )
        product1 = Product.objects.create(
            owner=user_1,
            title="Security services",
            description="Guarding services, patrols and inspections, access control, "
                        "concierge and receptionist services,"
                        " perimeter console operators, alarm response, and specialized client requested services.",
            latitude=0.0,
            longitude=0.0
        )
        product2 = Product.objects.create(
            owner=user_2,
            title="Cleaning services",
            description="Professional cleaning company for companies and individuals that offers services for offices,"
                        " apartments,"
                        " houses, buildings, hotels and all kinds of personal spaces",
            latitude=0.0,
            longitude=0.0
        )
        product3 = Product.objects.create(
            owner=user_3,
            title="Fruit",
            description="Organic and traditional fruits and vegetables, in bulk, in packs or in assorted "
                        "boxes of fruits and vegetables in different weights and compositions designed for the whole "
                        "week.",
            latitude=0.0,
            longitude=0.0
        )
        productImage1 = ProductImage.objects.create(
            name="security",
            product=product1,
            image="security.jpg"
        )
        productImage2 = ProductImage.objects.create(
            name="clean",
            product=product2,
            image="clean.jpg"
        )
        productImage3 = ProductImage.objects.create(
            name="fruit1",
            product=product3,
            image="fruit3.jpg"
        )
        productImage4 = ProductImage.objects.create(
            name="fruit2",
            product=product3,
            image="fruit5.jpg"
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
        pineapple_tag = Tag.objects.create(
            name="pineapple"
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
        security_tag = Tag.objects.create(
            name="security"
        )
        cleaning_tag = Tag.objects.create(
            name="cleaning"
        )
        cat_apple = Category.objects.create(
            name="fruit",
        )
        cat_apple.tag_children.set([apple_tag, apples_tag, pear_tag, pears_tag,pineapple_tag])
        cat_appliances = Category.objects.create(
            name="appliances",
        )

        cat_appliances.tag_children.set([dishwasher_tag, microwave_tag])
        cat_cleaning = Category.objects.create(
            name="cleaning",
        )
        cat_cleaning.tag_children.set([dishwasher_tag,cleaning_tag])
        cat_security=Category.objects.create(
            name="security",
        )
        cat_security.tag_children.set([security_tag])


        product4 = Product.objects.create(
            owner=user_3,
            title="Pineapple",
            description="Best pineapple on the market. Pineapple is packed full of fibre, vitamins and minerals and contains an enzyme "
                        "called bromelain. Discover why that makes this tropical fruit so healthy.",
            latitude=0.0,
            longitude=0.0,

        )
        productImage5=ProductImage.objects.create(
            name="pineapple",
            product=product4,
            image="pineapple.jpg"
        )

        product4.tag.set([apple_tag, apples_tag, pear_tag, pears_tag,pineapple_tag])
        product1.tag.set([security_tag])
        product2.tag.set([cleaning_tag,dishwasher_tag])
        product3.tag.set([apple_tag, apples_tag, pear_tag, pears_tag, pineapple_tag])
        product5 = Product.objects.create(
            owner=user_4,
            title="Microwave",
            description="ML2-EM09PA(BS) Microwave Oven with Smart Sensor, Position-Memory Turntable, Eco Mode,"
                        " and Sound On/Off function, 0.9Cu.ft/900W, Black Stainless Steel, 0.9 Cu Ft",
            latitude=2.0,
            longitude=3.0
        )
        product5.tag.set([dishwasher_tag, microwave_tag])
        productImage6=ProductImage.objects.create(
            name="microwave",
            product=product5,
            image="microwave.jpg"
        )
        client1 = User.objects.create(
            username="emina",
            password="complexpass",
            email="emina@gmail.com",
            first_name="Linguini",
            last_name="S",
        )
        client2 = User.objects.create(
            username="nico",
            password="complexpass",
            email="nico@gmail.com",
            first_name="Macaroni",
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
        e3 = Encounter.objects.create(
            client=client2,
            product=product3
        )
        # FormalOffer
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        FormalOffer.objects.create(
            encounterId = e,
            version = 2,
            contract = "Contract2",
            signedPdf = file_mock
        )
        FormalOffer.objects.create(
            encounterId=e3,
            version=1,
            contract="Contract",
            signedPdf=file_mock
        )
        FormalOffer.objects.create(
            encounterId = e2,
            version = 3,
            contract = "Contract",
            signedPdf = file_mock
        )
        Enterprise.objects.create(
            owner=user_1,
            NIF="2345678X",
            name="Securitas",
            contactInfo="security@gmail.com",
            description="Securitas USA's services include guarding services, patrols and inspections, access control, "
                        "concierge and receptionist services,"
                        " perimeter console operators, alarm response, and specialized client requested services."
                        "Securitas serves a wide range of customers in a variety of industries and customer segments.",
            profileImage="securityProfile.png",
            bannerImage="securityBanner.jpg"
        )
        Enterprise.objects.create(
            owner=user_2,
            NIF="21345678X",
            name="Bling",
            contactInfo="blingSpark@gmail.com",
            description="Cleaning or housekeeping required? Find affordable cleaners, cleaning ladies, housekeepers & gardeners."
                        "Professional cleaning company for companies and individuals that offers services for offices,"
                        " apartments,"
                        " houses, buildings, hotels and all kinds of personal spaces",
            profileImage="cleanProfile.png",
            bannerImage="cleanBanner.jpg"
        )
        Enterprise.objects.create(
            owner=user_3,
            NIF="21346578X",
            name="Vegefruit",
            contactInfo="vegefruit@gmail.com",
            description="In Vegefruit you will find fresh fruits, vegetables and other organic products directly from"
                        " the farmer. Organic and traditional fruits and vegetables, in bulk, in packs or in assorted "
                        "boxes of fruits and vegetables in different weights and compositions designed for the whole "
                        "week."
                        "With Vegefruit's advanced fruit and vegetable serch engine you can filter before order your"
                        " fruits and vegetables online by different criteria: price, province of origin, type of "
                        "growing, organic ... The savings by reducing the margin of brokering can thus be invested in "
                        "higher quality agriculture and a fairer price for all.",
            profileImage="fruitProfile.png",
            bannerImage="fruitBanner.jpg"
        )
        Enterprise.objects.create(
            owner=user_4,
            NIF="213456876X",
            name="TechnoMag",
            contactInfo="technomag@gmail.com",
            description="Our reputation is rooted in customer service. We specialize in offering high-quality, energy efficient kitchen and"
                        " laundry appliances. Choose our products and appliances and trust they'll handle your family's chores with care. ",
            profileImage="applianceProfile.png",
            bannerImage="applianceBanner.png"
        )
