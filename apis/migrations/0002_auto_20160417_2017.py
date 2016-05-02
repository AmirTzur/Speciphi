# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EbayLaptopAspect',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('aspect', models.CharField(max_length=30)),
                ('categories', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EbayLaptopFilter',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('filter', models.CharField(max_length=30)),
                ('categories', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Laptop',
        ),
    ]
