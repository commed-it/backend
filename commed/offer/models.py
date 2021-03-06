import uuid
from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class Encounter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'Encounter(id={self.id}, client={self.client}, product={self.product})'


class FormalOffer(models.Model):
    class State(models.TextChoices):
        SIGNED = 'SI', 'Signed'
        NOTSIGNED = 'NS', 'Not Signed'

    encounterId = models.ForeignKey(Encounter, on_delete=models.CASCADE, null=False, related_name="encounterId")
    version = models.IntegerField()
    contract = models.TextField()
    pdf = models.FileField(null=True)
    state = models.CharField(
        max_length=2,
        choices=State.choices,
        default=State.SIGNED,
    )


    def __str__(self):
        return f"""FormalOffer(encounterId ={self.encounterId}, version='{self.version}',
                               contract='{self.contract}', signedPdf='{self.pdf}', state={self.state})"""
