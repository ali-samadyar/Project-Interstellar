from django.db import models

# Create your models here.

class SSLCertificate(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    expiration_date = models.DateTimeField()
    remaining_days = models.IntegerField()

    def __str__(self):
        return self.domain