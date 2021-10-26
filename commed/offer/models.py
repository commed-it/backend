from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Encounter(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class FormalOffer(models.Model):
    encounterId = models.ForeignKey(Encounter, on_delete=models.CASCADE, null=False, related_name="encounterId")
    version = models.IntegerField()
    contract = models.TextField()
    signedPdf = models.FileField()

    def __str__(self):
        return f"""FormalOffer(encounterId ={self.encounterId}, version='{self.version}',
                               contract='{self.contract}', signedPdf='{self.signedPdf}')"""


