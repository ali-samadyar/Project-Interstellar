import subprocess
from django.shortcuts import render, redirect
from deviceHub.models import Device
from .models import VlanInventory
from django.http import JsonResponse
from netmiko import ConnectHandler
from .credentials import general_cred, f5_cred
import os
from django.contrib import messages


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


def vlan_manager(request):
    devices = Device.objects.all()
    vlans = VlanInventory.objects.all()

    if request.method == 'POST':
        vlan_id = request.POST.get('vlan_id')
        vlan_name = request.POST.get('vlan_name')
        selected_devices = request.POST.getlist('selected_devices')

        error_messages = []
        success_messages = []

        for device_ip in selected_devices:
            try:
                device = Device.objects.get(ip_address=device_ip)
                device = general_cred 
                device['ip'] = device_ip
                device['device_type'] = 'cisco_ios'
                connection = ConnectHandler(**device)
                vlan_command = f"vlan {vlan_id}\nname {vlan_name}"
                output = connection.send_config_set(vlan_command)
                connection.disconnect()

                if 'Error' in output:
                    error_messages.append(f"Failed to configure VLAN on device {device_ip}: {output}")
                else:
                    # Check if the VLAN already exists for this device
                    existing_vlan = VlanInventory.objects.filter(
                        vlan_name=vlan_name,
                        vlan_id=vlan_id,
                        devices=device
                    ).first()

                    if existing_vlan:
                        error_messages.append(f"VLAN {vlan_name} already exists for device {device_ip}")
                    else:
                        # Save the result in the database
                        vlan, created = VlanInventory.objects.get_or_create(
                            vlan_name=vlan_name,
                            vlan_id=vlan_id
                        )
                        vlan.devices.add(device)
                        success_messages.append(f"VLAN configured successfully on device {device_ip}")

            except Device.DoesNotExist:
                error_messages.append(f"Device with IP {device_ip} not found.")

        # Display messages in the template
        for error_message in error_messages:
            messages.error(request, error_message)
        for success_message in success_messages:
            messages.success(request, success_message)

        return redirect('vlan_manager')

    return render(request, 'vlan_manager.html', {'devices': devices, 'vlans': vlans})