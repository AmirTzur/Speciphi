# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0003_auto_20160410_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulteeaffiliations',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
        migrations.AlterUniqueTogether(
            name='consulteeaffiliations',
            unique_together=set([('consultationprocesses', 'selectiondatetime')]),
        ),
    ]
