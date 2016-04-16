# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0002_remove_amir_description'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Amir',
        ),
    ]
