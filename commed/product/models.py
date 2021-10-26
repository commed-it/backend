from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"Tag({self.name})"


class Category(models.Model):
    name = models.CharField(max_length=60)
    tag_children = models.ManyToManyField(Tag)

    def __str__(self):
        return f"Category({self.name})"


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=350)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return f"Product(owner={self.owner}, title={self.title})"


class ProductImage(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"ProductImage(name={self.name}, product={self.product})"
