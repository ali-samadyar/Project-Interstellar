# views.py
from django.shortcuts import render, redirect
from netmiko import ConnectHandler
from django.shortcuts import get_object_or_404
from deviceHub.models import Device
from .models import ConfigBackup
from .credentials import general_cred, f5_cred
from django.contrib import messages

def config_guardian(request, device_ip):
    device = get_object_or_404(Device, ip_address=device_ip)
    backups = ConfigBackup.objects.filter(device_ip=device.ip_address).order_by('-timestamp')
    selected_backup_id = request.GET.get('backup_id', None)
    backup_id = request.GET.get('backup_id')
    selected_backup = None
    if backup_id:
        selected_backup = get_object_or_404(ConfigBackup, id=backup_id)

    if request.method == 'POST':
        try:
            config_output = backup_config(device)
            if config_output is not None:
                # Save the backup to the database
                ConfigBackup.objects.create(device_ip=device.ip_address, config_data=config_output)
        except Exception as e:
            print(f"Failed to backup configuration for {device.ip_address}: {str(e)}")

    return render(request, 'configGuardian.html', {'device': device, 'backups': backups, 'selected_backup': selected_backup, 'selected_backup_id': selected_backup_id})


def backup_config(device):
    device_cred = general_cred
    device_cred['ip'] = device.ip_address

    if device.manufacturer == 'Cisco':
        device_cred['device_type'] = 'cisco_ios'
        return _backup_cisco_config(device_cred)
    elif device.manufacturer == 'Fortinet':
        device_cred['device_type'] = 'fortinet'
        return _backup_fortinet_config(device_cred)
    else:
        print(f"Unsupported device type: {device.device_type}")
        return None


def _backup_cisco_config(device_cred):
    try:
        net_connect = ConnectHandler(**device_cred)
        config_output = net_connect.send_command('show running-config')
        net_connect.disconnect()
        return config_output
    except Exception as e:
        print(f"Failed to backup Cisco configuration: {str(e)}")
        return None


def _backup_fortinet_config(device_cred):
    try:
        net_connect = ConnectHandler(**device_cred)
        config_output = net_connect.send_command('show full-configuration')
        net_connect.disconnect()
        return config_output
    except Exception as e:
        print(f"Failed to backup Fortinet configuration: {str(e)}")
        return None


def remove_backup(request, device_ip, backup_id):
    backup = get_object_or_404(ConfigBackup, id=backup_id)
    backup.delete()
    messages.success(request, f"Backup with ID {backup_id} has been removed successfully.")
    return redirect('config_guardian', device_ip=device_ip)

