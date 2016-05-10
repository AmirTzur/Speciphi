# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0004_auto_20160503_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Levelofuse',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'levelofuse',
            },
        ),
    ]
