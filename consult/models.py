from __future__ import unicode_literals

from django.db import models


class Entrance(models.Model):
    ip = models.CharField(max_length=24)
    country = models.CharField(max_length=45, blank=True, null=True)
    entrance_date_time = models.DateTimeField()
    exit_date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'entrance'


class Product(models.Model):
    name = models.CharField(unique=True, max_length=45)
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'product'


class ConsultationProcess(models.Model):
    entrance = models.ForeignKey('Entrance')
    product = models.ForeignKey('Product')
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'consultation_process'


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


class Use(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    id = models.IntegerField()
    name = models.CharField(max_length=45)
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'use'
        unique_together = (('product', 'id'), ('product', 'name'),)


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


class LevelOfUse(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    use = models.ForeignKey('Use')
    use_name = models.CharField(max_length=45)
    value = models.IntegerField()
    description = models.TextField()
    creation_date_time = models.DateTimeField()
    last_update = models.DateTimeField()

    class Meta:
        db_table = 'level_of_use'
        unique_together = (('product', 'use', 'value'),)


class Question(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    id = models.IntegerField()
    header = models.CharField(max_length=45)
    content = models.TextField()
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'question'
        unique_together = (('product', 'header'), ('product', 'id'),)


class Answer(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    question = models.ForeignKey('Question')
    question_header = models.CharField(max_length=45)
    question_content = models.TextField()
    id = models.IntegerField()
    name = models.CharField(max_length=25)
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'answer'
        unique_together = (('product', 'id'), ('product', 'question', 'name'),)
