from django.shortcuts import render
import requests
from django.http import JsonResponse

# Create your views here.


def subnet_calculator_function(request):
    if request.method == 'POST':
        subnet = request.POST.get('subnet')
        mask = request.POST.get('mask')
        url_api = f"https://networkcalc.com/api/ip/{subnet}/{mask}"
        print(url_api)
        response = requests.get(url_api)
        if response.status_code == 200:
            data = response.json()
            # print(data)
            address_data = data['address']
            cidr_notation = address_data['cidr_notation']
            subnet_bits = address_data['subnet_bits']
            subnet_mask = address_data['subnet_mask']
            wildcard_mask = address_data['wildcard_mask']
            network_address = address_data['network_address']
            broadcast_address = address_data['broadcast_address']
            assignable_hosts = address_data['assignable_hosts']
            first_assignable_host = address_data['first_assignable_host']
            last_assignable_host = address_data['last_assignable_host']

            data = {
                'cidr_notation': cidr_notation,
                'subnet_bits': subnet_bits,
                'subnet_mask': subnet_mask,
                'wildcard_mask': wildcard_mask,
                'network_address': network_address,
                'broadcast_address': broadcast_address,
                'assignable_hosts': assignable_hosts,
                'first_assignable_host': first_assignable_host,
                'last_assignable_host': last_assignable_host
            }

            return render(request, 'subnet_calc.html', {'data': data})
        
        else:
            error_message = response.json()['meta']['message'][0]
            return render(request, 'subnet_calc.html', {'error': error_message})
    else:
        return render(request, 'subnet_calc.html')

