import subprocess
from django.shortcuts import render
from deviceHub.models import Device
from django.http import JsonResponse
from netmiko import ConnectHandler
from .credentials import general_cred, f5_cred
import os


# Create your views here.
def device_data(request):
    devices = Device.objects.all().values_list( 'device_name', 'ip_address', 'manufacturer')
    context = {'devices': devices}
    return render(request, 'interface_mng.html', context)


def get_interface_info(request, device_ip):
    device = Device.objects.get(ip_address=device_ip)

    device = general_cred
    device['ip'] = device_ip

    if device['manufacturer'] == 'cisco':
        device['device_type'] = 'cisco_ios'
        connection = ConnectHandler(**device)
        command = 'show ip interface brief'
        output = connection.send_command(command)
        connection.disconnect()
        interfaces = {}
        for line in output.split('\n'):
            fields = line.split()
            if fields:
                interface = fields[0]
                ip_address = fields[1]
                status = fields[5]
                interfaces[interface] = {'ip_address': ip_address, 'status': status}
    elif device['manufacturer'] == 'fortinet':
        device['device_type'] = 'fortinet'
        connection = ConnectHandler(**device)
        command = 'get system interface'
        output = connection.send_command(command)
        connection.disconnect()
        interfaces = {}
        for line in output.split('\n'):
            fields = line.split()
            if fields:
                interface = fields[0]
                ip_address = fields[3]
                status = fields[4]
                interfaces[interface] = {'ip_address': ip_address, 'status': status}
    elif device['manufacturer'] == 'f5':
        device['device_type'] = 'f5'
        connection = ConnectHandler(**device)
        command = 'show net interface'
        output = connection.send_command(command)
        connection.disconnect()
        interfaces = {}
        for line in output.split('\n'):
            fields = line.split()
            if fields:
                interface = fields[0]
                ip_address = fields[1]
                status = fields[2]
                interfaces[interface] = {'ip_address': ip_address, 'status': status}


    return JsonResponse({'interfaces': interfaces})


def ping_device(request, device_ip):
    count = ' -c 2 '
    response = os.system("ping"+ count + device_ip)
    if response == 0:
        success = True
    else:
        success = False
    return JsonResponse({'success': success})
