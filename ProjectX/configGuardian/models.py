# models.py
from django.db import models
from deviceHub.models import Device

class ConfigBackup(models.Model):
    device_ip = models.GenericIPAddressField()
    config_data = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device_ip 