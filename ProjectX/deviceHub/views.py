from django.shortcuts import get_object_or_404, redirect, render
from .forms import DeviceForm
from .models import Device
from django.http import JsonResponse
from django.db.models import Q
import json


def device_hub(request):
    devices = Device.objects.all()
    return render(request, 'devicehub.html', {'devices': devices})


def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('devicehub')
    else:
        form = DeviceForm()

    return render(request, 'add_device.html', {'form': form})