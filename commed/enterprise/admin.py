# Register your models here.
from django.contrib import admin

from .models import Enterprise


# Register your models here.

class EnterpriseAdmin(admin.ModelAdmin):
    pass


admin.site.register(Enterprise, EnterpriseAdmin)
