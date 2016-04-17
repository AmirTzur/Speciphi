from django.contrib import admin

from apis.models import EbayLaptopAspect, EbayLaptopFilter
from apis.admin import EbayLaptopAspectAdmin, EbayLaptopFilterAdmin

# Register your models here.


# Register API APP models

admin.site.register(EbayLaptopAspect, EbayLaptopAspectAdmin)
admin.site.register(EbayLaptopFilter, EbayLaptopFilterAdmin)
