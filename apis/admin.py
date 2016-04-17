from django.contrib import admin

from .models import EbayLaptopAspect, EbayLaptopFilter

# Register your models here.


class EbayLaptopAspectAdmin(admin.ModelAdmin):
    fields = ('aspect', 'categories')
    list_display = ('aspect', 'categories')


class EbayLaptopFilterAdmin(admin.ModelAdmin):
    fields = ('filter', 'categories')
    list_display = ('filter', 'categories')

