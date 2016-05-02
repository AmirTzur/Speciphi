from django.db import models

# Create your models here.


class EbayLaptopDeal(models.Model):

    price = models.IntegerField()

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return self.price



