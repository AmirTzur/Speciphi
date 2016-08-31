# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConsulteeAffiliation',
            fields=[
                ('key', models.AutoField(serialize=False, primary_key=True)),
                ('selection_date_time', models.DateTimeField()),
                ('checked', models.IntegerField()),
            ],
            options={
                'managed': False,
                'db_table': 'consultee_affiliation',
            },
        ),
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('key', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.IntegerField()),
                ('name', models.CharField(max_length=45)),
                ('description', models.TextField()),
                ('creation_date_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'affiliation',
            },
        ),
        migrations.CreateModel(
            name='ConsultationProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date_time', models.DateTimeField()),
                ('end_date_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'consultation_process',
            },
        ),
        migrations.CreateModel(
            name='Entrance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=24)),
                ('country', models.CharField(max_length=45, blank=True, null=True)),
                ('entrance_date_time', models.DateTimeField()),
                ('exit_date_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'entrance',
            },
        ),
        migrations.CreateModel(
            name='LevelOfUse',
            fields=[
                ('key', models.AutoField(serialize=False, primary_key=True)),
                ('use_name', models.CharField(max_length=45)),
                ('value', models.IntegerField()),
                ('description', models.TextField()),
                ('creation_date_time', models.DateTimeField()),
                ('last_update', models.DateTimeField()),
            ],
            options={
                'db_table': 'level_of_use',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=45)),
                ('creation_date_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Use',
            fields=[
                ('key', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.IntegerField()),
                ('name', models.CharField(max_length=45)),
                ('creation_date_time', models.DateTimeField()),
                ('product', models.ForeignKey(to='consult.Product')),
            ],
            options={
                'db_table': 'use',
            },
        ),
        migrations.AddField(
            model_name='levelofuse',
            name='product',
            field=models.ForeignKey(to='consult.Product'),
        ),
        migrations.AddField(
            model_name='levelofuse',
            name='use',
            field=models.ForeignKey(to='consult.Use'),
        ),
        migrations.AddField(
            model_name='consultationprocess',
            name='entrance',
            field=models.ForeignKey(to='consult.Entrance'),
        ),
        migrations.AddField(
            model_name='consultationprocess',
            name='product',
            field=models.ForeignKey(to='consult.Product'),
        ),
        migrations.AddField(
            model_name='affiliation',
            name='product',
            field=models.ForeignKey(to='consult.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='use',
            unique_together=set([('product', 'name'), ('product', 'id')]),
        ),
        migrations.AlterUniqueTogether(
            name='levelofuse',
            unique_together=set([('product', 'use', 'value')]),
        ),
        migrations.AlterUniqueTogether(
            name='affiliation',
            unique_together=set([('product', 'name'), ('product', 'id')]),
        ),
    ]
