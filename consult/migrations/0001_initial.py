# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entrances',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('ip', models.CharField(max_length=16)),
                ('country', models.CharField(blank=True, null=True, max_length=45)),
                ('entrancedatetime', models.DateTimeField(db_column='entranceDateTime')),
                ('exitdatetime', models.DateTimeField(blank=True, db_column='exitDateTime', null=True)),
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
                ('image', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Products',
            },
        ),
    ]
