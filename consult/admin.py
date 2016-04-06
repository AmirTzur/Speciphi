from django.contrib import admin

from apis.models import Laptop
from apis.admin import LaptopAdmin
# Register your models here.


admin.site.register(Laptop, LaptopAdmin)
