from django.contrib import admin

from .models import Laptop

# Register your models here.


class LaptopAdmin(admin.ModelAdmin):
    fields = ('title', 'brand', 'date')
    list_display = ('title', 'brand')

