from django import forms
from .models import Device

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_name', 'ip_address', 'device_type', 'manufacturer', 'model', 'location', 'rack_loc']
