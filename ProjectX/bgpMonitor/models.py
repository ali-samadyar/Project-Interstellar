from django.db import models

# Create your models here.



class BGPCheckResult(models.Model):
    as_number = models.CharField(max_length=255)
    as_name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    country = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.as_number} - {self.as_name}'
