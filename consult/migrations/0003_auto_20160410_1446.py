# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0002_consultationprocesses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=45)),
                ('description', models.TextField(max_length=300)),
                ('image', models.TextField(null=True, blank=True)),
                ('creationdatetime', models.DateTimeField(db_column='creationDateTime')),
                ('products', models.ForeignKey(db_column='Products_id', to='consult.Products')),
            ],
            options={
                'db_table': 'affiliations',
            },
        ),
        migrations.AlterUniqueTogether(
            name='affiliations',
            unique_together=set([('products', 'name')]),
        ),
    ]
