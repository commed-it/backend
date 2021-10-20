from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Enterprise(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="owner")
    NIF = models.CharField(max_length=30)
    name = models.CharField(max_length=128)
    contactInfo = models.CharField(max_length=256)
    description = models.TextField(help_text='Description about the entity. It can be provided HTML')

    def __str__(self):
        return f"""Enterprise(owner={self.owner}, NIF='{self.NIF}',
                              name='{self.name}', contactInfo='Contact Info'
                              descripton='{self.description}')"""
