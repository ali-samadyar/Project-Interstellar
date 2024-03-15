from django import forms
from .models import SMTPConfiguration

class SMTPConfigurationForm(forms.ModelForm):
    class Meta:
        model = SMTPConfiguration
        fields = ['smtp_name', 'smtp_sender', 'smtp_password', 'smtp_server', 'smtp_server_port']
