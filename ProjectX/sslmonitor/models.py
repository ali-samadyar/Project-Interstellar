from django.db import models

# Create your models here.

class SSLCertificate(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    expiration_date = models.DateTimeField()
    remaining_days = models.IntegerField()

    def __str__(self):
        return f'{self.domain} - {self.remaining_days}'
    

class EmailConfig(models.Model):
    smtp_name = models.CharField(max_length=100)
    receiver = models.EmailField()

    def __str__(self):
        return f"{self.smtp_name} - {self.receiver}"