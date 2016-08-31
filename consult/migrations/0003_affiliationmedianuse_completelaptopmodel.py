# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consult', '0002_auto_20160830_1408'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliationMedianUse',
            fields=[
                ('cluster', models.IntegerField(primary_key=True, serialize=False)),
                ('word_processing_office_applications', models.IntegerField(db_column='Word Processing & Office Applications')),
                ('audio_editing', models.IntegerField(db_column='Audio Editing')),
                ('video_watching', models.IntegerField(db_column='Video Watching')),
                ('video_editing', models.IntegerField(db_column='Video Editing')),
                ('pictures_editing', models.IntegerField(db_column='Pictures Editing')),
                ('number_3d_design', models.IntegerField(db_column='3D Design')),
                ('developing_programming', models.IntegerField(db_column='Developing & Programming')),
                ('portability', models.IntegerField(db_column='Portability')),
                ('storage', models.IntegerField(db_column='Storage')),
                ('gaming', models.IntegerField(db_column='Gaming')),
                ('life_cycle', models.IntegerField(db_column='Life Cycle')),
                ('programs_running', models.IntegerField(db_column='Programs Running')),
                ('everyday_computing', models.IntegerField(db_column='Everyday Computing')),
                ('style_design', models.IntegerField(db_column='Style & Design')),
            ],
            options={
                'db_table': 'affiliation_median_use',
            },
        ),
        migrations.CreateModel(
            name='CompleteLaptopModel',
            fields=[
                ('key', models.AutoField(primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=30, db_column='Model')),
                ('brand', models.CharField(max_length=15, db_column='Brand')),
                ('line', models.CharField(max_length=45, db_column='Line')),
                ('gpu', models.CharField(max_length=30, db_column='GPU')),
                ('screen_size', models.FloatField(db_column='Screen.Size')),
                ('screen_resolution', models.CharField(max_length=15, db_column='Screen.Resolution')),
                ('touch_screen', models.CharField(max_length=5, db_column='Touch.Screen')),
                ('processor', models.CharField(max_length=30, db_column='Processor')),
                ('memory', models.IntegerField(db_column='Memory')),
                ('battery', models.CharField(max_length=30, db_column='Battery')),
                ('storagessd', models.IntegerField(db_column='StorageSSD')),
                ('storagehdd', models.IntegerField(db_column='StorageHDD')),
                ('dimensions', models.CharField(max_length=25, db_column='Dimensions')),
                ('weight', models.FloatField(db_column='Weight')),
                ('color', models.CharField(max_length=15, db_column='Color')),
                ('operating_system', models.CharField(max_length=15, db_column='Operating.System')),
                ('rankcpu', models.FloatField(db_column='rankCPU')),
                ('rankgpu', models.FloatField(db_column='rankGPU')),
                ('rankram', models.FloatField(db_column='rankRAM')),
                ('rankhd', models.FloatField(db_column='rankHD')),
                ('rankbattery', models.FloatField(db_column='rankBattery')),
                ('rankweight', models.FloatField(db_column='rankWeight')),
                ('dealamazonrank', models.IntegerField(null=True, blank=True, db_column='dealAmazonRank')),
                ('lowestprice', models.FloatField(db_column='lowestPrice')),
                ('image_url', models.CharField(max_length=2083)),
                ('clusterid', models.IntegerField(db_column='clusterId')),
                ('filtergpu', models.CharField(max_length=30, db_column='filterGPU')),
                ('filtercpu', models.CharField(max_length=30, db_column='filterCPU')),
                ('filtercapacity', models.IntegerField(db_column='filterCapacity')),
                ('offers', models.CharField(max_length=2083)),
                ('overallrank', models.FloatField(db_column='overallRank')),
                ('mobilityrank', models.FloatField(db_column='mobilityRank')),
            ],
            options={
                'db_table': 'complete_laptop_model',
            },
        ),
    ]
