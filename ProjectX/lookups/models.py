# models.py
from django.db import models

class LookupHistory(models.Model):
    hostname = models.CharField(max_length=255)
    registrar = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    abuse_email = models.EmailField(blank=True, null=True)
    cname_record = models.JSONField(blank=True, null=True)
    a_record = models.JSONField(blank=True, null=True, default=dict)
    mx_record = models.JSONField(blank=True, null=True)
    ns_record = models.JSONField(blank=True, null=True)
    soa_record = models.JSONField(blank=True, null=True)
    

    def __str__(self):
        return self.hostname
