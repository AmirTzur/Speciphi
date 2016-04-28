from django.contrib import admin

from apis.models import EbayLaptopAspect, EbayLaptopDeal
from apis.admin import EbayLaptopAspectAdmin, EbayLaptopDealAdmin

# Register your models here.


# Register API APP models

admin.site.register(EbayLaptopAspect, EbayLaptopAspectAdmin)
admin.site.register(EbayLaptopDeal, EbayLaptopDealAdmin)
