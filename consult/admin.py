from django.contrib import admin

from apis.models import EbayLaptopDeal
from apis.admin import EbayLaptopDealAdmin

# Register your models here.


# Register API APP models

admin.site.register(EbayLaptopDeal, EbayLaptopDealAdmin)
