# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('key', models.AutoField(primary_key=True, serialize=False)),
                ('question_header', models.CharField(max_length=45)),
                ('question_content', models.TextField()),
                ('id', models.IntegerField()),
                ('name', models.CharField(max_length=25)),
                ('creation_date_time', models.DateTimeField()),
                ('product', models.ForeignKey(to='consult.Product')),
            ],
            options={
                'db_table': 'answer',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.IntegerField()),
                ('header', models.CharField(max_length=45)),
                ('content', models.TextField()),
                ('creation_date_time', models.DateTimeField()),
                ('product', models.ForeignKey(to='consult.Product')),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='consult.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together=set([('product', 'header'), ('product', 'id')]),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('product', 'id'), ('product', 'question', 'name')]),
        ),
    ]
