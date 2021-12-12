import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from enterprise.models import Enterprise


class Command(BaseCommand):
    help = "Adds super user if it does not exist, with username and password as the configuration"

    def handle(self, *args, **kwargs):
        admin_username = os.getenv("DJANGO_ADMIN_USERNAME")
        admin_password = os.getenv("DJANGO_ADMIN_PASSWORD")
        admin_email = os.getenv("DJANGO_ADMIN_EMAIL")
        if not User.objects.filter(username=admin_username).exists():
            User.objects.create()
            admin = User.objects.create_superuser(
                email=admin_email, username=admin_username, password=admin_password
            )
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            Enterprise.objects.create(
                owner=admin,
                NIF="0000000X",
                name="Admin page",
                contactInfo=admin_email,
                description="Commed administration account. Feel free contact us if you have any problem."
            )
            self.stdout.write('Admin successfully created!')
        else:
            self.stdout.write('Admin was already in the database!')
