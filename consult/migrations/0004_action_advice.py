# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0003_affiliationmedianuse_completelaptopmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('key', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.IntegerField(blank=True, null=True)),
                ('object_id', models.IntegerField(blank=True, null=True)),
                ('content', models.CharField(blank=True, null=True, max_length=50)),
                ('creation_date_time', models.DateTimeField()),
                ('consultation_process', models.ForeignKey(to='consult.ConsultationProcess')),
                ('entrance', models.ForeignKey(to='consult.Entrance')),
            ],
            options={
                'db_table': 'action',
            },
        ),
        migrations.CreateModel(
            name='Advice',
            fields=[
                ('key', models.AutoField(serialize=False, primary_key=True)),
                ('advisor_id', models.IntegerField()),
                ('header', models.CharField(max_length=35)),
                ('content', models.TextField()),
                ('triger', models.CharField(max_length=25)),
                ('triger_id', models.IntegerField()),
            ],
            options={
                'db_table': 'advice',
            },
        ),
    ]
