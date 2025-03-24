from django.contrib import admin
from .models import HousingUnit, HousingAllocation

# Register your models here.

admin.site.register(HousingUnit)
admin.site.register(HousingAllocation)