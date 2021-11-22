from django.contrib import admin

# Register your models here.
from .models import Encounter


# Register your models here.

class EncounterAdmin(admin.ModelAdmin):
    pass


admin.site.register(Encounter, EncounterAdmin)
