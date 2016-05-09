from django.contrib import admin

from .models import Entrances, Products, Consultationprocesses, Affiliations, Consulteeaffiliations


class EntrancesAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip', 'country', 'entrancedatetime', 'exitdatetime')


admin.site.register(Entrances, EntrancesAdmin)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creationdatetime', 'image')


admin.site.register(Products, ProductsAdmin)


class ConsultationprocessesAdmin(admin.ModelAdmin):
    list_display = ('id', 'entrances', 'products', 'startdatetime', 'enddatetime')


admin.site.register(Consultationprocesses, ConsultationprocessesAdmin)


class AffiliationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'products', 'name', 'description', 'image', 'creationdatetime')


admin.site.register(Affiliations, AffiliationsAdmin)


class ConsulteeaffiliationsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'entrances_id', 'products_id', 'consultationprocesses', 'affiliations', 'selectiondatetime', 'checked')


admin.site.register(Consulteeaffiliations, ConsulteeaffiliationsAdmin)
