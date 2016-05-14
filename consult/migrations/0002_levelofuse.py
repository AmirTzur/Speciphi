# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Levelofuse',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('Uses_id', models.IntegerField()),
                ('Uses_name', models.CharField(max_length=45, blank=True)),
                ('value', models.IntegerField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'levelofuse',
            },
        ),
    ]
