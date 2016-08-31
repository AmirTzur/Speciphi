from __future__ import unicode_literals

from django.db import models


class Entrance(models.Model):
    ip = models.CharField(max_length=24)
    country = models.CharField(max_length=45, blank=True, null=True)
    entrance_date_time = models.DateTimeField()
    exit_date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'entrance'


class Product(models.Model):
    name = models.CharField(unique=True, max_length=45)
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'product'


class ConsultationProcess(models.Model):
    entrance = models.ForeignKey('Entrance')
    product = models.ForeignKey('Product')
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'consultation_process'


class Affiliation(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    id = models.IntegerField()
    name = models.CharField(max_length=45)
    description = models.TextField()
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'affiliation'
        unique_together = (('product', 'name'), ('product', 'id'),)


class Use(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    id = models.IntegerField()
    name = models.CharField(max_length=45)
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'use'
        unique_together = (('product', 'id'), ('product', 'name'),)


class ConsulteeAffiliation(models.Model):
    key = models.AutoField(primary_key=True)
    entrance = models.ForeignKey('Entrance')
    product = models.ForeignKey('Product')
    consultation_process = models.ForeignKey('ConsultationProcess')
    affiliation = models.ForeignKey('Affiliation')
    selection_date_time = models.DateTimeField()
    checked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'consultee_affiliation'
        unique_together = (('consultation_process', 'selection_date_time'),)


class LevelOfUse(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    use = models.ForeignKey('Use')
    use_name = models.CharField(max_length=45)
    value = models.IntegerField()
    description = models.TextField()
    creation_date_time = models.DateTimeField()
    last_update = models.DateTimeField()

    class Meta:
        db_table = 'level_of_use'
        unique_together = (('product', 'use', 'value'),)


class Question(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    id = models.IntegerField()
    header = models.CharField(max_length=45)
    content = models.TextField()
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'question'
        unique_together = (('product', 'header'), ('product', 'id'),)


class Answer(models.Model):
    key = models.AutoField(primary_key=True)
    product = models.ForeignKey('Product')
    question = models.ForeignKey('Question')
    question_header = models.CharField(max_length=45)
    question_content = models.TextField()
    id = models.IntegerField()
    name = models.CharField(max_length=25)
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'answer'
        unique_together = (('product', 'id'), ('product', 'question', 'name'),)


class CompleteLaptopModel(models.Model):
    key = models.AutoField(primary_key=True)
    model = models.CharField(db_column='Model', max_length=30)  # Field name made lowercase.
    brand = models.CharField(db_column='Brand', max_length=15)  # Field name made lowercase.
    line = models.CharField(db_column='Line', max_length=45)  # Field name made lowercase.
    gpu = models.CharField(db_column='GPU', max_length=30)  # Field name made lowercase.
    screen_size = models.FloatField(db_column='Screen.Size')
    screen_resolution = models.CharField(db_column='Screen.Resolution',
                                         max_length=15)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    touch_screen = models.CharField(db_column='Touch.Screen',
                                    max_length=5)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    processor = models.CharField(db_column='Processor', max_length=30)  # Field name made lowercase.
    memory = models.IntegerField(db_column='Memory')  # Field name made lowercase.
    battery = models.CharField(db_column='Battery', max_length=30)  # Field name made lowercase.
    storagessd = models.IntegerField(db_column='StorageSSD')  # Field name made lowercase.
    storagehdd = models.IntegerField(db_column='StorageHDD')  # Field name made lowercase.
    dimensions = models.CharField(db_column='Dimensions', max_length=25)  # Field name made lowercase.
    weight = models.FloatField(db_column='Weight')  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=15)  # Field name made lowercase.
    operating_system = models.CharField(db_column='Operating.System',
                                        max_length=15)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rankcpu = models.FloatField(db_column='rankCPU')  # Field name made lowercase.
    rankgpu = models.FloatField(db_column='rankGPU')  # Field name made lowercase.
    rankram = models.FloatField(db_column='rankRAM')  # Field name made lowercase.
    rankhd = models.FloatField(db_column='rankHD')  # Field name made lowercase.
    rankbattery = models.FloatField(db_column='rankBattery')  # Field name made lowercase.
    rankweight = models.FloatField(db_column='rankWeight')  # Field name made lowercase.
    dealamazonrank = models.IntegerField(db_column='dealAmazonRank', blank=True,
                                         null=True)  # Field name made lowercase.
    lowestprice = models.FloatField(db_column='lowestPrice')  # Field name made lowercase.
    image_url = models.CharField(max_length=2083)
    clusterid = models.IntegerField(db_column='clusterId')  # Field name made lowercase.
    filtergpu = models.CharField(db_column='filterGPU', max_length=30)  # Field name made lowercase.
    filtercpu = models.CharField(db_column='filterCPU', max_length=30)  # Field name made lowercase.
    filtercapacity = models.IntegerField(db_column='filterCapacity')  # Field name made lowercase.
    offers = models.CharField(max_length=2083)
    overallrank = models.FloatField(db_column='overallRank')  # Field name made lowercase.
    mobilityrank = models.FloatField(db_column='mobilityRank')  # Field name made lowercase.

    class Meta:
        db_table = 'complete_laptop_model'


class AffiliationMedianUse(models.Model):
    cluster = models.IntegerField(primary_key=True)
    word_processing_office_applications = models.IntegerField(
        db_column='Word Processing & Office Applications')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    audio_editing = models.IntegerField(
        db_column='Audio Editing')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    video_watching = models.IntegerField(
        db_column='Video Watching')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    video_editing = models.IntegerField(
        db_column='Video Editing')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pictures_editing = models.IntegerField(
        db_column='Pictures Editing')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    number_3d_design = models.IntegerField(
        db_column='3D Design')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it wasn't a valid Python identifier.
    developing_programming = models.IntegerField(
        db_column='Developing & Programming')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    portability = models.IntegerField(db_column='Portability')  # Field name made lowercase.
    storage = models.IntegerField(db_column='Storage')  # Field name made lowercase.
    gaming = models.IntegerField(db_column='Gaming')  # Field name made lowercase.
    life_cycle = models.IntegerField(
        db_column='Life Cycle')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    programs_running = models.IntegerField(
        db_column='Programs Running')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    everyday_computing = models.IntegerField(
        db_column='Everyday Computing')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    style_design = models.IntegerField(
        db_column='Style & Design')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        db_table = 'affiliation_median_use'


class Advice(models.Model):
    key = models.AutoField(primary_key=True)
    advisor_id = models.IntegerField()
    header = models.CharField(max_length=35)
    content = models.TextField()
    triger = models.CharField(max_length=25)
    triger_id = models.IntegerField()

    class Meta:
        db_table = 'advice'


class Action(models.Model):
    key = models.AutoField(primary_key=True)
    entrance = models.ForeignKey('Entrance')
    consultation_process = models.ForeignKey('ConsultationProcess')
    name = models.CharField(max_length=50)
    type = models.IntegerField(blank=True, null=True)
    object_id = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=50, blank=True, null=True)
    creation_date_time = models.DateTimeField()

    class Meta:
        db_table = 'action'
