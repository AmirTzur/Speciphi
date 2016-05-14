from __future__ import unicode_literals

from django.db import models


# why to use "managed = False":
# http://stackoverflow.com/questions/7625674/utility-of-managed-false-option-in-django-models
#
class Entrances(models.Model):
    def __str__(self):
        return 'Entrances Obj: ' + str(self.id)

    ip = models.CharField(max_length=16)
    country = models.CharField(max_length=45, blank=True, null=True)
    entrancedatetime = models.DateTimeField(db_column='entranceDateTime')
    exitdatetime = models.DateTimeField(db_column='exitDateTime', blank=True, null=True)

    class Meta:
        db_table = 'Entrances'


class Products(models.Model):
    def __str__(self):
        return 'Products Obj: ' + str(self.name)

    name = models.CharField(unique=True, max_length=45)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')
    # Should use ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)
    # and install pillow package
    # image = models.ImageField(upload_to='productsImages/', height_field=None, width_field=None)
    image = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Products'


class Consultationprocesses(models.Model):
    def __str__(self):
        return 'Consultationprocesses Obj: ' + str(self.id)

    entrances = models.ForeignKey('Entrances', db_column='Entrances_id')
    products = models.ForeignKey('Products', db_column='Products_id')
    startdatetime = models.DateTimeField(db_column='startDateTime')
    enddatetime = models.DateTimeField(db_column='endDateTime', blank=True, null=True)

    class Meta:
        db_table = 'consultationprocesses'


class Affiliations(models.Model):
    def __str__(self):
        return 'Affiliations Obj: ' + str(self.name)

    products = models.ForeignKey('Products', db_column='Products_id')
    name = models.CharField(max_length=45)
    description = models.TextField(max_length=300)
    image = models.TextField(blank=True, null=True)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')

    class Meta:
        db_table = 'affiliations'
        unique_together = (('products', 'name'),)


class Consulteeaffiliations(models.Model):
    def __str__(self):
        return 'Consulteeaffiliations Obj: ' + str(self.id)

    entrances_id = models.IntegerField(db_column='Entrances_id')
    products_id = models.IntegerField(db_column='Products_id')
    consultationprocesses = models.ForeignKey(Consultationprocesses,
                                              db_column='consultationProcesses_id')
    affiliations = models.ForeignKey(Affiliations, db_column='Affiliations_id')
    selectiondatetime = models.DateTimeField(db_column='selectionDateTime')
    checked = models.BooleanField()

    class Meta:
        db_table = 'consulteeaffiliations'
        unique_together = (('consultationprocesses', 'selectiondatetime'),)


class Levelofuse(models.Model):
    # def __str__(self):
    #     return 'Levelofuse Obj: ' + str(self.Uses_id), str(self.Uses_name)
    #
    Uses_id = models.IntegerField()
    Uses_name = models.CharField(max_length=45, blank=True)
    value = models.IntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'levelofuse'

###############################################################################################

# class Entrances(models.Model):
#     ip = models.CharField(max_length=24)
#     country = models.CharField(max_length=45, blank=True, null=True)
#     entrancedatetime = models.DateTimeField(db_column='entranceDateTime')  # Field name made lowercase.
#     exitdatetime = models.DateTimeField(db_column='exitDateTime', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'entrances'
#
#
# class Products(models.Model):
#     name = models.CharField(unique=True, max_length=45)
#     creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
#     imageurl = models.CharField(db_column='imageUrl', max_length=2083, blank=True,
#                                 null=True)  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'products'
#
#
# class Consultationprocesses(models.Model):
#     entrances = models.ForeignKey('Entrances', db_column='Entrances_id')  # Field name made lowercase.
#     products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
#     startdatetime = models.DateTimeField(db_column='startDateTime')  # Field name made lowercase.
#     enddatetime = models.DateTimeField(db_column='endDateTime', blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'consultationprocesses'
#
#
# class Affiliations(models.Model):
#     products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
#     ID = models.IntegerField()
#     name = models.CharField(max_length=45)
#     description = models.TextField()
#     imageurl = models.CharField(db_column='imageUrl', max_length=2083, blank=True,
#                                 null=True)  # Field name made lowercase.
#     creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'affiliations'
#         unique_together = (('products', 'ID'), ('products', 'name'),)

#
# class Uses(models.Model):
#     products = models.ForeignKey(Products, db_column='Products_id')  # Field name made lowercase.
#     ID = models.IntegerField()
#     name = models.CharField(max_length=45)
#     imageurl = models.CharField(db_column='imageUrl', max_length=2083, blank=True,
#                                 null=True)  # Field name made lowercase.
#     creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'uses'
#         unique_together = (('products', 'ID'), ('products', 'name'),)
#
#
# class Consulteeaffiliations(models.Model):
#     entrances_id = models.IntegerField(db_column='Entrances_id')  # Field name made lowercase.
#     products = models.ForeignKey(Products, db_column='Products_id')  # Field name made lowercase.
#     consultationprocesses = models.ForeignKey(Consultationprocesses,
#                                               db_column='consultationProcesses_id')  # Field name made lowercase.
#     affiliations = models.ForeignKey(Affiliations, to_field="ID",
#                                      db_column='Affiliations_id')  # Field name made lowercase.
#     selectiondatetime = models.DateTimeField(db_column='selectionDateTime')  # Field name made lowercase.
#     checked = models.IntegerField()
#
#     class Meta:
#         db_table = 'consulteeaffiliations'
#         unique_together = (('consultationprocesses', 'selectiondatetime'),)

#
# class Affiliationuses(models.Model):
#     products = models.ForeignKey('Uses', db_column='Products_id')  # Field name made lowercase.
#     affiliations = models.ForeignKey(Affiliations, db_column='Affiliations_id')  # Field name made lowercase.
#     uses = models.ForeignKey('Uses', db_column='Uses_id')  # Field name made lowercase.
#     fittinglevel = models.FloatField(db_column='fittingLevel')  # Field name made lowercase.
#     lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'affiliationuses'
#         unique_together = (('Products_id', 'Affiliations_id', 'Uses_id'),)
#
#
# class Levelofuse(models.Model):
#     creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
#     products = models.ForeignKey('Uses', db_column='Products_id')  # Field name made lowercase.
#     uses = models.ForeignKey('Uses', db_column='Uses_id')  # Field name made lowercase.
#     uses_name = models.CharField(db_column='Uses_name', max_length=45)  # Field name made lowercase.
#     value = models.IntegerField()
#     name = models.CharField(max_length=45, blank=True, null=True)
#     description = models.TextField()
#     lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'levelofuse'
#         unique_together = (('Products_id', 'Uses_id', 'value'),)
#
#
# class Consulteeuses(models.Model):
#     entrances_id = models.IntegerField(db_column='Entrances_id')  # Field name made lowercase.
#     products = models.ForeignKey('Levelofuse', db_column='Products_id')  # Field name made lowercase.
#     consultationprocesses = models.ForeignKey(Consultationprocesses,
#                                               db_column='consultationProcesses_id')  # Field name made lowercase.
#     uses = models.ForeignKey('Levelofuse', db_column='Uses_id')  # Field name made lowercase.
#     levelofuse_value = models.ForeignKey('Levelofuse', db_column='levelofUse_value')  # Field name made lowercase.
#     selectiondatetime = models.DateTimeField(db_column='selectionDateTime')  # Field name made lowercase.
#     checked = models.IntegerField()
#     checkedbyuser = models.IntegerField(db_column='checkedByUser')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'consulteeuses'
#         unique_together = (('consultationProcesses_id', 'Uses_id', 'levelofUse_value', 'selectionDateTime'),)
#
#
# class Affiliationlevelofuses(models.Model):
#     products = models.ForeignKey('Levelofuse', db_column='Products_id')  # Field name made lowercase.
#     affiliations = models.ForeignKey('Affiliations', db_column='Affiliations_id')  # Field name made lowercase.
#     uses = models.ForeignKey('Levelofuse', db_column='Uses_id')  # Field name made lowercase.
#     levelofuse_value = models.ForeignKey('Levelofuse', db_column='levelofUse_value')  # Field name made lowercase.
#     lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.
#
#     class Meta:
#         db_table = 'affiliationlevelofuses'
#         unique_together = (('Affiliations_id', 'Uses_id'),)
