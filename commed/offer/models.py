from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Encounter(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)