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
        form = DeviceForm() # an empty form

    return render(request, 'add_device.html', {'form': form})



def get_device_info(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    device_data = {
        'id': device.id,
        'device_name': device.device_name,
        'ip_address': device.ip_address,
        'device_type': device.device_type,
        'manufacturer': device.manufacturer,
        'model': device.model,
        'location': device.location,
        'rack_loc': device.rack_loc,
    }
    return JsonResponse(device_data)

def update_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            device = form.save()
            return redirect('devicehub')
    else:
        form = DeviceForm(instance=device)

    return JsonResponse({'status': 'error', 'form': form.as_p()})



def remove_device(request):
    if request.method == 'POST':
        device_id = request.POST.get('device_id')
        Device.objects.filter(id=device_id).delete()

    return redirect('devicehub')