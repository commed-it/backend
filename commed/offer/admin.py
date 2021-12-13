from django.contrib import admin

# Register your models here.
from .models import Encounter, FormalOffer


# Register your models here.

class EncounterAdmin(admin.ModelAdmin):
    pass

class FormalOfferAdmin(admin.ModelAdmin):
    pass


admin.site.register(Encounter, EncounterAdmin)
admin.site.register(FormalOffer, FormalOfferAdmin)
