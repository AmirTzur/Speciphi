from django.contrib import admin

from .models import EbayLaptopDeal

# Register your models here.

class EbayLaptopDealAdmin(admin.ModelAdmin):
    # I didn't test yet!!!
    list_display = [f.name for f in EbayLaptopDeal._meta.get_fields()]



