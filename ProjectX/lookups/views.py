from django.shortcuts import render
import requests
import datetime
from .models import LookupHistory

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
            'creation_date': whois_response.get('whois', {}).get('registry_created_date') if whois_response.get('whois', {}).get('registry_created_date') is not None else 'null',
            'expiration_date': whois_response.get('whois', {}).get('registry_expiration_date') if whois_response.get('whois', {}).get('registry_expiration_date') is not None else 'null',
            'abuse_email': whois_response.get('whois', {}).get('abuse_email') if whois_response.get('whois', {}).get('abuse_email') is not None else 'null',
        }
        lookup_data = {
            'hostname': lookup_response.get('hostname'),
            'records': lookup_response.get('records', {}),
        }
        #extracting the data from the response (dictionary) and storing it in a list
        ns_records = [{'nameserver': ns_record.get('nameserver')} for ns_record in lookup_data.get('records', {}).get('NS', []) if ns_record.get('nameserver') is not None]
        a_records = [a_record.get('address') for a_record in lookup_data.get('records', {}).get('A', [])]
        cname_records = [cname_record.get('cname') for cname_record in lookup_data.get('records', {}).get('CNAME', [])]
        mx_records = [{'exchange': mx_record.get('exchange'), 'priority': mx_record.get('priority')} for mx_record in lookup_data.get('records', {}).get('MX', [])]
        soa_records = [{'mname': soa_record.get('mname'), 'hostmaster': soa_record.get('hostmaster')} for soa_record in lookup_data.get('records', {}).get('SOA', [])]

        # Save or update the history
        history_entry, created = LookupHistory.objects.update_or_create(
            hostname=whois_data['hostname'],
            defaults={
                'registrar': whois_data['registrar'],
                'creation_date': datetime.datetime.strptime(whois_data['creation_date'], "%Y-%m-%dT%H:%M:%S%z") if whois_data['creation_date'] != 'null' else None,
                'expiration_date': datetime.datetime.strptime(whois_data['expiration_date'], "%Y-%m-%dT%H:%M:%S%z") if whois_data['expiration_date'] != 'null' else None,
                'abuse_email': whois_data['abuse_email'],
                'a_record': a_records[0] if a_records else None,
                'cname_record': cname_records[0] if cname_records else None,
                'mx_record': mx_records[0] if mx_records else None,
                'ns_record': ns_records,
                'soa_record': soa_records[0] if soa_records else None,
                # 'last_update': datetime.datetime.now(),
            }
        )

    # Load history for the table
    history = LookupHistory.objects.all()

    return render(request, 'lookups.html', {'history': history, 'whois_data': {}, 'lookup_data': {}})

    # return render(request, 'lookups.html')