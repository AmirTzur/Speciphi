from django.db import models

# Create your models here.


class EbayLaptopAspect(models.Model):

    aspect = models.CharField(max_length=30)
    categories = models.CharField(max_length=200)
    # updated = models.DateTimeField('Date published')

    # class Meta:
    #     ordering = ('-date',)
    #     get_latest_by = 'date'

    def __str__(self):
        return self.aspect


class EbayLaptopFilter(models.Model):

    filter = models.CharField(max_length=30)
    categories = models.CharField(max_length=200)
    # updated = models.DateTimeField('Date published')

    def __str__(self):
        return self.title


# class EbayLaptopFilter(models.Model):
#
#     title = models.CharField(max_length=200)
#     #
#     brand = models.CharField(max_length=30)
#     #
#     description = models.TextField()
#     url = models.CharField(max_length=400)
#     date = models.DateTimeField('Date published')
#     status = models.IntegerField(default=1)
#
#     class Meta:
#         ordering = ('-date',)
#         get_latest_by = 'date'
#
#     def __str__(self):
#         return self.title



