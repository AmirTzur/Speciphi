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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('startdatetime', models.DateTimeField(db_column='startDateTime')),
                ('enddatetime', models.DateTimeField(null=True, db_column='endDateTime', blank=True)),
            ],
            options={
                'db_table': 'consultationprocesses',
            },
        ),
        migrations.CreateModel(
            name='Consulteeaffiliations',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('entrances_id', models.IntegerField(db_column='Entrances_id')),
                ('products_id', models.IntegerField(db_column='Products_id')),
                ('selectiondatetime', models.DateTimeField(db_column='selectionDateTime')),
                ('checked', models.BooleanField()),
                ('affiliations', models.ForeignKey(to='consult.Affiliations', db_column='Affiliations_id')),
                ('consultationprocesses', models.ForeignKey(to='consult.Consultationprocesses', db_column='consultationProcesses_id')),
            ],
            options={
                'db_table': 'consulteeaffiliations',
            },
        ),
        migrations.CreateModel(
            name='Entrances',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('ip', models.CharField(max_length=16)),
                ('country', models.CharField(null=True, blank=True, max_length=45)),
                ('entrancedatetime', models.DateTimeField(db_column='entranceDateTime')),
                ('exitdatetime', models.DateTimeField(null=True, db_column='exitDateTime', blank=True)),
            ],
            options={
                'db_table': 'Entrances',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
            field=models.ForeignKey(to='consult.Entrances', db_column='Entrances_id'),
        ),
        migrations.AddField(
            model_name='consultationprocesses',
            name='products',
            field=models.ForeignKey(to='consult.Products', db_column='Products_id'),
        ),
        migrations.AddField(
            model_name='affiliations',
            name='products',
            field=models.ForeignKey(to='consult.Products', db_column='Products_id'),
        ),
        migrations.AlterUniqueTogether(
            name='consulteeaffiliations',
            unique_together=set([('consultationprocesses', 'selectiondatetime')]),
        ),
        migrations.AlterUniqueTogether(
            name='affiliations',
            unique_together=set([('products', 'name')]),
        ),
    ]
