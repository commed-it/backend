import json
import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from chat.models import Message
from offer.models import Encounter, FormalOffer
from product.models import Product, Category, Tag, ProductImage
from enterprise.models import Enterprise
from unittest.mock import MagicMock
from django.core.files import File


class Command(BaseCommand):
    help = "Adds things to the database. In catalan"

    def handle(self, *args, **kwargs):
        user_1 = User.objects.create_user(
            id=1,
            username="user1",
            password="complexpass",
            email="commed.noreply@gmail.com",
            first_name="Joan",
            last_name="Doe",
        )
        user_2 = User.objects.create_user(
            id=2,
            username="user2",
            password="complexpass",
            email="commed.noreply@gmail.com",
            first_name="Jana",
            last_name="Joe",
        )
        user_3 = User.objects.create_user(
            id=3,
            username="user3",
            password="complexpass",
            email="commed.noreply@gmail.com",
            first_name="Jaume",
            last_name="Oliver",
        )
        user_4 = User.objects.create_user(
            id=4,
            username="user4",
            password="complexpass",
            email="commed.noreply@gmail.com",
            first_name="Blanca",
            last_name="Crews",
        )
        product1 = Product.objects.create(
            owner=user_1,
            title="Serveis de seguretat",  # "Security services",
            description="Serves de vigilància, patrulles, inspeccions, controls d'accés, conseges i serveis de recepció,"
                        "vigilància de perímetre, resposta d'alarma i servies espacialitzats al client.",
            latitude=0.0,
            longitude=0.0
        )
        product2 = Product.objects.create(
            owner=user_2,
            title="Serveis de neteja",
            description="Empresa de neteja professional, tant per a individus com per a empreses. Treballem amb oficines,"
                        "apartaments, cases, edificis, hotels i altres tipus d'espais.",
            latitude=0.0,
            longitude=0.0
        )
        product3 = Product.objects.create(
            owner=user_3,
            title="Fruita",
            description="Fruites i verdures orgàniques i tradicional. Venem a l'engrós, en pacs, o en caixes de fruita i"
                        "vegetals de diferents pesos en composicions pensades per una setmana.",
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
            name="poma"
        )
        apples_tag = Tag.objects.create(
            name="pomes"
        )
        pear_tag = Tag.objects.create(
            name="pera"
        )
        pineapple_tag = Tag.objects.create(
            name="pinya"
        )
        pears_tag = Tag.objects.create(
            name="peres"
        )
        dishwasher_tag = Tag.objects.create(
            name="rentaplats"
        )
        microwave_tag = Tag.objects.create(
            name="microones"
        )
        security_tag = Tag.objects.create(
            name="seguretat"
        )
        cleaning_tag = Tag.objects.create(
            name="neteja"
        )
        cat_apple = Category.objects.create(
            name="fruita",
        )
        cat_apple.tag_children.set([apple_tag, apples_tag, pear_tag, pears_tag, pineapple_tag])
        cat_appliances = Category.objects.create(
            name="electrodomèstics",
        )

        cat_appliances.tag_children.set([dishwasher_tag, microwave_tag])
        cat_cleaning = Category.objects.create(
            name="neteja",
        )
        cat_cleaning.tag_children.set([dishwasher_tag, cleaning_tag])
        cat_security = Category.objects.create(
            name="seguretat",
        )
        cat_security.tag_children.set([security_tag])

        product4 = Product.objects.create(
            owner=user_3,
            title="Pinya",
            description="La millor pinya de tot el mercat. La pinya està plena de fibra, vitamina, i minerals que contenen"
                        "l'enzim de bromelain. Descobreix el perquè aquesta fruita tropical és tan sana.",
            latitude=0.0,
            longitude=0.0,

        )
        productImage5 = ProductImage.objects.create(
            name="pineapple",
            product=product4,
            image="pineapple.jpg"
        )

        product4.tag.set([apple_tag, apples_tag, pear_tag, pears_tag, pineapple_tag])
        product1.tag.set([security_tag])
        product2.tag.set([cleaning_tag, dishwasher_tag])
        product3.tag.set([apple_tag, apples_tag, pear_tag, pears_tag, pineapple_tag])
        product5 = Product.objects.create(
            owner=user_4,
            title="Microones",
            description="ML2-EM09PA(BS) Forn Microones amb Sensor intel·ligent, posicicó de memòria per a horaris,"
                        "Mode Eco i funció On/Off de sonido, 0.9Cu.ft/900W, Negre briillant, 0.9 Cu Ft",
            latitude=2.0,
            longitude=3.0
        )
        product5.tag.set([dishwasher_tag, microwave_tag])
        productImage6 = ProductImage.objects.create(
            name="microones",
            product=product5,
            image="microwave.jpg"
        )

        e = Encounter.objects.create(
            client=user_4,
            product=product1
        )
        # Little chat

        msg1 = Message.objects.create(
            author=user_4,
            msg=json.dumps({'user': 4, 'type': 'message', 'message': "M'agradaria això."}),
            channel_context=e
        )
        msg2 = Message.objects.create(
            author=user_1,
            msg=json.dumps({'user': 1, 'type': 'message', 'message': "Quan estàs disposat a pagar?"}),
            channel_context=e
        )
        msg3 = Message.objects.create(
            author=user_4,
            msg=json.dumps({'user': 4, 'type': 'message', 'message': 'Que tal gratis?'}),
            channel_context=e
        )
        msg2 = Message.objects.create(
            author=user_1,
            msg=json.dumps({'user': 1, 'type': 'message', 'message': "Perfecte!"}),
            channel_context=e
        )

        e2 = Encounter.objects.create(
            client=user_4,
            product=product2
        )
        e3 = Encounter.objects.create(
            client=user_2,
            product=product3
        )
        # FormalOffer
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.pdf'
        FormalOffer.objects.create(
            encounterId=e,
            version=2,
            contract="Contract2",
            pdf=file_mock
        )
        FormalOffer.objects.create(
            encounterId=e3,
            version=1,
            contract="Contract",
            pdf=file_mock
        )
        FormalOffer.objects.create(
            encounterId=e2,
            version=3,
            contract="Contract",
            pdf=file_mock
        )
        Enterprise.objects.create(
            owner=user_1,
            NIF="2345678X",
            name="Securitas",
            contactInfo="security@gmail.com",
            description="Serves de vigilància, patrulles, inspeccions, controls d'accés, conseges i serveis de recepció,"
                        "vigilància de perímetre, resposta d'alarma i servies espacialitzats al client."
                        "Securitas dona un àmplia gama de serveis a diferents tipus d'usuaris provenents de moltes  indústries"
                        "diferents.",
            profileImage="securityProfile.png",
            bannerImage="securityBanner.jpg",
            location="4455 Landing Lange, APT 4 Louisville, KY 40018-1234"
        )
        Enterprise.objects.create(
            owner=user_2,
            NIF="21345678X",
            name="Bling",
            contactInfo="blingSpark@gmail.com",
            description="Necessites neteja? Troba bones dones de la neteja a bon preu, així com també jardiners."
                        "Som una empresa de neteja professional que oferim els nostres servies tan a empreses com "
                        "individus per qualsevol tipus de neteja, ja sigui per a oficines, cases, apartaments, edificies,"
                        "hotels, i altres tipus d'espais.",
            profileImage="cleanProfile.png",
            bannerImage="cleanBanner.jpg",
            location="90210 Broadway Blvd. Nashville, TN 37011-5678"
        )
        Enterprise.objects.create(
            owner=user_3,
            NIF="21346578X",
            name="Vegefruit",
            contactInfo="vegefruit@gmail.com",
            description="A Vegefruit trobaràs tota la fruita fresca, vegetals i altres tipus de productes orgànics"
                        "directament provinents del pagés. "
                        "Fruites i verdures orgàniques i tradicionals. Venem a l'engrós, en pacs, o en caixes de fruita i"
                        "vegetals de diferents pesos en composicions pensades per una setmana.",
            profileImage="fruitProfile.png",
            bannerImage="fruitBanner.jpg",
            location="SGT 6543 N 9th Street APO, AA 33608-1234"
        )
        Enterprise.objects.create(
            owner=user_4,
            NIF="213456876X",
            name="TechnoMag",
            contactInfo="technomag@gmail.com",
            description="La nostra reputació es basa en els nostres serveis als clients. Ens especialitzem en oferir "
                        "electrodomèstics d'alta qualitat, així com també eficientment energètics per a la vostra cuina"
                        "o bugaderia. Tria algun desl nostres productes i electrodomèstics i confia en que sabrem"
                        "portar els vostres feines domèstiques amb cura.",
            profileImage="applianceProfile.png",
            bannerImage="applianceBanner.jpg",
            location="4455 Landing Lange, APT 4, Nashville, TN 37011-5678"
        )
