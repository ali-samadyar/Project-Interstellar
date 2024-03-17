from django.contrib import admin
from .models import SSLCertificate, EmailConfig

admin.site.register(SSLCertificate)
admin.site.register(EmailConfig)
# Register your models here.
