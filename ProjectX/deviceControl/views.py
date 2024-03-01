import subprocess
from django.shortcuts import render
from deviceHub.models import Device
from django.http import JsonResponse
from netmiko import ConnectHandler
from .credentials import general_cred
import os


# Create your views here.
def device_data(request):
    devices = Device.objects.all().values_list( 'device_name', 'ip_address')
    context = {'devices': devices}
    return render(request, 'interface_mng.html', context)


def get_interface_info(request, device_ip):
    device = general_cred
    device['ip'] = device_ip
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
    return JsonResponse({'interfaces': interfaces})


def ping_device(request, device_ip):
    response = os.system("ping " + device_ip)
    if response == 0:
        success = True
    else:
        success = False
    return JsonResponse({'success': success})

# def interface_action(request, device_ip, interface, action):
#     device = general_cred
#     device['ip'] = device_ip
#     device['device_type'] = 'cisco_ios'

#     connection = ConnectHandler(**device)
#     if action == 'shutdown':
#         command = f'interface {interface}; shutdown'
#     elif action == 'no_shutdown':
#         command = f'interface {interface}; no shutdown'
#     else:
#         raise ValueError(f'Invalid action: {action}')
#     connection.send_config_set(command, read_timeout=90.0)
#     connection.disconnect()
#     return JsonResponse({'success': True})