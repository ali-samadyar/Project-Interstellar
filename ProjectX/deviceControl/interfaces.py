import netmiko


# Define the device details
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.200.101',
    'username': 'astrox',
    'password': 'P@ssw0rd',
}

# Connect to the device
connection = netmiko.ConnectHandler(**device)

# Send the shutdown command to the interface
interface = 'ethernet0/1'  # Replace with the actual interface name
command = [
    f'interface {interface}',
    'no shutdown',
]
output = connection.send_config_set(command, read_timeout=90.0)

# Disconnect from the device
connection.disconnect()

print(output)