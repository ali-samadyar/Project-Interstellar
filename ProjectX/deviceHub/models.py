# models.py
from django.db import models

class Device(models.Model):
    device_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    device_type = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    model = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    rack_loc = models.CharField(max_length=255, blank=True, null=True)
