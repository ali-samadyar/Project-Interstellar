from django.db import models
from deviceHub.models import Device

# Create your models here.


class VlanInventory(models.Model):
    vlan_name = models.CharField(max_length=50)
    vlan_id = models.PositiveIntegerField()
    devices = models.ManyToManyField(Device)