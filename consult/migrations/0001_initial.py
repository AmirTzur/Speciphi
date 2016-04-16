# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amir',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=200)),
                ('brand', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=400)),
                ('date', models.DateTimeField(verbose_name='Date published')),
                ('status', models.IntegerField(default=1)),
            ],
            options={
                'get_latest_by': 'date',
                'ordering': ('-date',),
            },
        ),
    ]
