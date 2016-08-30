from __future__ import unicode_literals

from django.db import models


# ---------------------------------------------------------------------------------------------------------------------------------#
# Table `djaroodb`.`Entrance`
# ---------------------------------------------------------------------------------------------------------------------------------#
class Entrance(models.Model):
    ip = models.CharField(max_length=24)
    country = models.CharField(max_length=45, blank=True, null=True)
    entrance_date_time = models.DateTimeField()
    exit_date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'entrance'


# ---------------------------------------------------------------------------------------------------------------------------------#
# Table `djaroodb`.`Product`
# ---------------------------------------------------------------------------------------------------------------------------------#
class Product(models.Model):
    name = models.CharField(unique=True, max_length=45)
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'product'


# ---------------------------------------------------------------------------------------------------------------------------------#
# Table `djaroodb`.`consultation_process`
# ---------------------------------------------------------------------------------------------------------------------------------#
class ConsultationProcess(models.Model):
    entrance = models.ForeignKey('Entrance')
    product = models.ForeignKey('Product')
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'consultation_process'


# ---------------------------------------------------------------------------------------------------------------------------------#
# Table `djaroodb`.`Affiliation`
# ---------------------------------------------------------------------------------------------------------------------------------#
class Affiliation(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    id = models.IntegerField()
    name = models.CharField(max_length=45)
    description = models.TextField()
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'affiliation'
        unique_together = (('product', 'name'), ('product', 'id'),)


# ---------------------------------------------------------------------------------------------------------------------------------#
# Table `djaroodb`.`Uses`
# ---------------------------------------------------------------------------------------------------------------------------------#
class Use(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    id = models.IntegerField()
    name = models.CharField(max_length=45)
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'use'
        unique_together = (('product', 'id'), ('product', 'name'),)


# ---------------------------------------------------------------------------------------------------------------------------------#
# Table `djaroodb`.`consultee_affiliation`
# ---------------------------------------------------------------------------------------------------------------------------------#
class ConsulteeAffiliation(models.Model):
    key = models.AutoField(primary_key=True)
    entrance = models.ForeignKey('Entrance')
    product = models.ForeignKey('Product')
    consultation_process = models.ForeignKey('ConsultationProcess')
    affiliation = models.ForeignKey('Affiliation')
    selection_date_time = models.DateTimeField()
    checked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'consultee_affiliation'
        unique_together = (('consultation_process', 'selection_date_time'),)

