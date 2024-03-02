# views.py
from django.shortcuts import render
import requests

def lookups(request):
    if request.method == 'POST':
        hostname = request.POST.get('url_Input')

        # Fetch data from API 1 (whois)
        whois_url = f'https://networkcalc.com/api/dns/whois/{hostname}'
        whois_response = requests.get(whois_url).json()

        # Fetch data from API 2 (lookup)
        lookup_url = f'https://networkcalc.com/api/dns/lookup/{hostname}'
        lookup_response = requests.get(lookup_url).json()

        # Extract data from responses
        whois_data = {
            'hostname': whois_response.get('hostname'),
            'registrar': whois_response.get('whois', {}).get('registrar'),
            'creation_date': whois_response.get('whois', {}).get('registry_created_date'),
            'expiration_date': whois_response.get('whois', {}).get('registry_expiration_date'),
            'abuse_email': whois_response.get('whois', {}).get('abuse_email'),
        }

        lookup_data = {
            'hostname': lookup_response.get('hostname'),
            'records': lookup_response.get('records', {}),
        }

        return render(request, 'lookups.html', {'whois_data': whois_data, 'lookup_data': lookup_data})

    return render(request, 'lookups.html')
