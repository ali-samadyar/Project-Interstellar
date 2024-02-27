from urllib.request import Request, urlopen
import json

def bgp_get_response(asn):
    url = f'https://api.asrank.caida.org/v2/restful/asns/{asn}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    request = Request(url, headers=headers)
    asn_response = urlopen(request).read().decode('utf-8')
    asn_response = json.loads(asn_response)

    if 'data' in asn_response and asn_response['data']['asn']:
        asn_data = asn_response['data']['asn']
        asn_info = {
            'as_number': asn_data['asn'],
            'as_name': asn_data['asnName'],
            'source': asn_data['source'],
            'longitude': asn_data['longitude'],
            'latitude': asn_data['latitude'],
            'country': asn_data['country']['iso'],
        }
        return asn_info
    else:
        return None