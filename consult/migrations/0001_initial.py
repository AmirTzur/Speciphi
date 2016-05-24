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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('description', models.TextField(max_length=300)),
                ('image', models.TextField(blank=True, null=True)),
                ('creationdatetime', models.DateTimeField(db_column='creationDateTime')),
            ],
            options={
                'db_table': 'affiliations',
            },
        ),
        migrations.CreateModel(
            name='Consultationprocesses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('startdatetime', models.DateTimeField(db_column='startDateTime')),
                ('enddatetime', models.DateTimeField(blank=True, null=True, db_column='endDateTime')),
            ],
            options={
                'db_table': 'consultationprocesses',
            },
        ),
        migrations.CreateModel(
            name='Consulteeaffiliations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ip', models.CharField(max_length=16)),
                ('country', models.CharField(max_length=45, null=True, blank=True)),
                ('entrancedatetime', models.DateTimeField(db_column='entranceDateTime')),
                ('exitdatetime', models.DateTimeField(blank=True, null=True, db_column='exitDateTime')),
            ],
            options={
                'db_table': 'Entrances',
            },
        ),
        migrations.CreateModel(
            name='Levelofuse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('Uses_id', models.IntegerField()),
                ('Uses_name', models.CharField(max_length=45, blank=True)),
                ('value', models.IntegerField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'levelofuse',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('creationdatetime', models.DateTimeField(db_column='creationDateTime')),
                ('image', models.TextField(blank=True, null=True)),
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
