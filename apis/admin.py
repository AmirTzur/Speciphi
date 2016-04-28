from django.contrib import admin

from .models import EbayLaptopAspect, EbayLaptopDeal

# Register your models here.


class EbayLaptopAspectAdmin(admin.ModelAdmin):
    fields = ('aspect', 'categories')
    list_display = ('aspect', 'categories')


class EbayLaptopDealAdmin(admin.ModelAdmin):
    list_display = [f.name for f in EbayLaptopDeal._meta.get_fields()]



