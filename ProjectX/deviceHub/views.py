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


def search(request):
    query = request.GET.get('q')
    if query:
        devices = Device.objects.filter(
            Q(device_name__icontains=query)
            | Q(ip_address__icontains=query)
            | Q(device_type__icontains=query)
            | Q(manufacturer__icontains=query)
            | Q(model__icontains=query)
            | Q(location__icontains=query)
            | Q(rack_loc__icontains=query)
        )
        devices_json = []
        for device in devices:
            device_dict = {
                "model": "devices.device",
                "pk": device.pk,
                "fields": {
                    "device_name": device.device_name,
                    "ip_address": str(device.ip_address),
                    "device_type": device.device_type,
                    "manufacturer": device.manufacturer,
                    "model": device.model,
                    "location": device.location,
                    "rack_loc": device.rack_loc,
                }
            }
            devices_json.append(device_dict)
        data = json.dumps(devices_json)
        return JsonResponse(data, safe=False)

    else:

        return render(request, 'devices.html')
    

def device_list_all(request):
    devices = list(Device.objects.values())
    devices_json = json.dumps(devices)
    return JsonResponse(devices_json, safe=False)
    # return render(request, 'devicehub.html', {'devices_json': devices_json})

def get_device_detail(request, id):
    device = get_object_or_404(Device, pk=id)
    data = {
        'device_name': device.device_name,
        'ip_address': device.ip_address,
        'device_type': device.device_type,
        'manufacturer': device.manufacturer,
        'model': device.model,
        'location': device.location,
        'rack_loc': device.rack_loc,
    }
    return JsonResponse(data)


def fetch_device(request, id):
    device = get_object_or_404(Device, pk=id)
    data = {
        'device_name': device.device_name,
        'ip_address': device.ip_address,
        # Add more fields as needed
    }
    return JsonResponse(data)

def edit_device(request, id):
    device = get_object_or_404(Device, pk=id)
    if request.method == 'POST':
        device.device_name = request.POST.get('device_name')
        device.ip_address = request.POST.get('ip_address')
        # Update more fields as needed
        device.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})