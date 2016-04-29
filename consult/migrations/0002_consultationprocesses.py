# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consultationprocesses',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('startdatetime', models.DateTimeField(db_column='startDateTime')),
                ('enddatetime', models.DateTimeField(blank=True, db_column='endDateTime', null=True)),
                ('entrances', models.ForeignKey(to='consult.Entrances', db_column='Entrances_id')),
                ('products', models.ForeignKey(to='consult.Products', db_column='Products_id')),
            ],
            options={
                'db_table': 'consultationprocesses',
            },
        ),
    ]
