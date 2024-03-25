import platform
from django.shortcuts import render, redirect
from deviceHub.models import Device
from .models import VlanInventory
from django.http import JsonResponse
from netmiko import ConnectHandler
from .credentials import general_cred, f5_cred
import os
from django.contrib import messages
from urllib.parse import unquote


def device_data(request):
    # create a tuple of device data (not all fields)
    devices = Device.objects.all().values_list( 'device_name', 'ip_address', 'manufacturer', 'device_type')
    #create a dictionary of device data (key: devices / value: device data (Django QuerySet object))
    context = {'devices': devices}
    return render(request, 'interface_mng.html', context)

def get_interface_info(request, device_ip):
    # look for the device with the given IP address
    device = Device.objects.get(ip_address=device_ip)
    manufacturer = device.manufacturer
    device_cred = general_cred
    device_cred['ip'] = device_ip

    if manufacturer == 'Cisco':
        device_cred['device_type'] = 'cisco_ios'
        connection = ConnectHandler(**device_cred)
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
    elif manufacturer == 'Fortinet':
        device_cred['device_type'] = 'fortinet'
        connection = ConnectHandler(**device_cred)
        command = 'get system interface'
        output = connection.send_command(command)
        connection.disconnect()
        interfaces = {}
        interfaces = output.split('== [ ')[1:] # split the output into sections (disacard anything before ==)


        # this part just extract NAME of the interfaces
        parsed_interfaces = [ 
            {'name': name.split('   ')[0], 'ip': 'N/A', 'status': 'N/A'} # create a dictionary for each interafce
            for name in (section.split('name: ')[1].split('\n')[0] for section in interfaces) 
        ]
        for idx, section in enumerate(interfaces): 
            if ' ip: ' in section:
                name = section.split('name: ')[1].split('   ')[0] #delimiter would be removed form the list (which is 'name: ')
                ip = section.split(' ip: ')[1].split('   ')[0]
                status = section.split(' status: ')[1].split('   ')[0]
                parsed_interfaces[idx]['name'] = name
                parsed_interfaces[idx]['ip'] = ip
                parsed_interfaces[idx]['status'] = status
                interfaces = parsed_interfaces
                
    return JsonResponse({'interfaces': interfaces})

def device_interface_action(request, device_ip, encoded_interface_name, action):
    interface = unquote(encoded_interface_name)
    if request.method == 'POST':
        device = Device.objects.get(ip_address=device_ip)
        device_cred = general_cred
        device_cred['ip'] = device_ip
             
        try:
            if device.manufacturer == 'Cisco':
                # interface = unquote(interface)
                # print(interface)
                device_type = 'cisco_ios'
                if action == 'shut':
                    commands = [' interface ' + interface + '\n', 'shutdown']
                else:
                    commands = [' interface ' + interface + '\n', 'no shutdown']
            elif device.manufacturer == 'Fortinet':
                device_type = 'fortinet'
                if action == 'shut':
                    commands = ['config system interface', 'edit ' + interface, 'set status down', 'end']
                else:
                    commands = ['config system interface', 'edit ' + interface, 'set status up', 'end']
            else:
                return JsonResponse({'success': False, 'message': 'Unsupported device manufacturer.'})
            device_cred['device_type'] = device_type
            connection = ConnectHandler(**device_cred)
            connection.enable()
            output = connection.send_config_set(commands)
            connection.disconnect()
            return JsonResponse({'success': True, 'message': 'Interface status changed successfully.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method. Use POST.'})

def ping_device(request, device_ip):
    count = ' -n 2 ' if platform.system().lower() == 'windows' else ' -c 2 '
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
                device_cred = general_cred 
                device_cred['ip'] = device_ip
                device_cred['device_type'] = 'cisco_ios'
                connection = ConnectHandler(**device_cred)
                output = connection.send_config_set([f"vlan {vlan_id}", f"name {vlan_name}"])
                connection.disconnect()
                output_lines = output.splitlines()
                error_detected = any("Error" in line for line in output_lines)
                if error_detected:
                    error_messages.append(f"Failed to configure VLAN on device {device_ip}: {output}")

                else:
                    # Save the result in the database
                    vlan, created = VlanInventory.objects.get_or_create(
                        vlan_name = vlan_name,
                        vlan_id = vlan_id
                        # selected_devices=device
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

    return render(request, 'vlan_manager.html', {'devices': devices, 'vlans': vlans})

def show_command_runner(request):
    devices = Device.objects.all()

    if request.method == 'POST':
        selected_device_ids = request.POST.getlist('selected_devices')
        command = request.POST.get('command')

        if not command.strip().lower().startswith('show'):
            error = "Invalid command. Please enter a command starting with 'SHOW'."
            return render(request, 'show_command_runner.html', {'devices': devices, 'error': error})

        results = {}

        for device_id in selected_device_ids:
            try:
                device = Device.objects.get(id=device_id)
                device_cred = general_cred
                device_cred['ip'] = device.ip_address
                device_cred['device_type'] = 'cisco_ios'               
                connection = ConnectHandler(**device_cred)
                result = connection.send_command(command)
                connection.disconnect()
                results[device.ip_address] = {'result': result, 'error': None}
            except Exception as e:
                results[device.ip_address] = {'result': None, 'error': str(e)}

        return render(request, 'show_command_runner.html', {'devices': devices, 'results': results, 'command': command})

    return render(request, 'show_command_runner.html', {'devices': devices})

def write_memory(request):
    devices = Device.objects.all()

    if request.method == 'POST':
        selected_devices = request.POST.getlist('selected_devices')
        error_messages = []
        success_messages = []

        for device_id in selected_devices:
            try:
                device = Device.objects.get(id=device_id)
                device_cred = general_cred
                device_cred['ip'] = device.ip_address
                device_cred['device_type'] = 'cisco_ios'
                
                connection = ConnectHandler(**device_cred)
                output = connection.send_command('write memory')
                connection.disconnect()
                
                success_messages.append(f"Write memory successful on device {device.device_name}")
            except Exception as e:
                error_messages.append(f"Error writing memory on device {device.device_name}: {str(e)}")

        for error_message in error_messages:
            messages.error(request, error_message)
        for success_message in success_messages:
            messages.success(request, success_message)

        return redirect('write_memory')

    return render(request, 'write_job.html', {'devices': devices})