from __future__ import unicode_literals

from django.db import models


# why to use "managed = False":
# http://stackoverflow.com/questions/7625674/utility-of-managed-false-option-in-django-models

class Entrances(models.Model):
    ip = models.CharField(max_length=16)
    country = models.CharField(max_length=45, blank=True, null=True)
    entrancedatetime = models.DateTimeField(db_column='entranceDateTime')  # Field name made lowercase.
    exitdatetime = models.DateTimeField(db_column='exitDateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Entrances'


class Products(models.Model):
    name = models.CharField(unique=True, max_length=45)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
    # Should use ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)
    # and install pillow package
    # image = models.ImageField(upload_to='productsImages/', height_field=None, width_field=None)
    image = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Products'


class Consultationprocesses(models.Model):
    entrances = models.ForeignKey('Entrances', db_column='Entrances_id')  # Field name made lowercase.
    products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
    startdatetime = models.DateTimeField(db_column='startDateTime')  # Field name made lowercase.
    enddatetime = models.DateTimeField(db_column='endDateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'consultationprocesses'


class Affiliations(models.Model):
    products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
    name = models.CharField(max_length=45)
    description = models.TextField(max_length=300)
    image = models.TextField(blank=True, null=True)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        db_table = 'affiliations'
        unique_together = (('products', 'name'),)
