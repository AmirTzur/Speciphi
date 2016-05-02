from django.contrib import admin

from apis.models import EbayLaptopDeal
from apis.admin import EbayLaptopDealAdmin

# Register your models here.


# Register API APP models

admin.site.register(EbayLaptopDeal, EbayLaptopDealAdmin)
from .models import Entrances, Products, Consultationprocesses


class EntrancesAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'country', 'entrancedatetime', 'exitdatetime')


admin.site.register(Entrances, EntrancesAdmin)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creationdatetime')


admin.site.register(Products, ProductsAdmin)


class ConsultationprocessesAdmin(admin.ModelAdmin):
    list_display = ('id', 'entrances', 'products', 'startdatetime', 'enddatetime')


admin.site.register(Consultationprocesses, ConsultationprocessesAdmin)
