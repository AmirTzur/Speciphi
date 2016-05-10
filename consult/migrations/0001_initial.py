# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliations',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('description', models.TextField(max_length=300)),
                ('image', models.TextField(null=True, blank=True)),
                ('creationdatetime', models.DateTimeField(db_column='creationDateTime')),
            ],
            options={
                'db_table': 'affiliations',
            },
        ),
        migrations.CreateModel(
            name='Consultationprocesses',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('startdatetime', models.DateTimeField(db_column='startDateTime')),
                ('enddatetime', models.DateTimeField(db_column='endDateTime', null=True, blank=True)),
            ],
            options={
                'db_table': 'consultationprocesses',
            },
        ),
        migrations.CreateModel(
            name='Entrances',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('ip', models.CharField(max_length=16)),
                ('country', models.CharField(null=True, blank=True, max_length=45)),
                ('entrancedatetime', models.DateTimeField(db_column='entranceDateTime')),
                ('exitdatetime', models.DateTimeField(db_column='exitDateTime', null=True, blank=True)),
            ],
            options={
                'db_table': 'Entrances',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('creationdatetime', models.DateTimeField(db_column='creationDateTime')),
                ('image', models.TextField(null=True, blank=True)),
            ],
            options={
                'db_table': 'Products',
            },
        ),
        migrations.AddField(
            model_name='consultationprocesses',
            name='entrances',
            field=models.ForeignKey(db_column='Entrances_id', to='consult.Entrances'),
        ),
        migrations.AddField(
            model_name='consultationprocesses',
            name='products',
            field=models.ForeignKey(db_column='Products_id', to='consult.Products'),
        ),
        migrations.AddField(
            model_name='affiliations',
            name='products',
            field=models.ForeignKey(db_column='Products_id', to='consult.Products'),
        ),
        migrations.AlterUniqueTogether(
            name='affiliations',
            unique_together=set([('products', 'name')]),
        ),
    ]
