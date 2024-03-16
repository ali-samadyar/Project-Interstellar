import ssl
import socket
import datetime

# def get_ssl_certificate_info(url_input):
#     url_input = url_input.lower()
    
#     try:
#         context = ssl.create_default_context()
        
#         with socket.create_connection((url_input, 443)) as sock:
#             with context.wrap_socket(sock, server_hostname=url_input) as ssl_sock:
#                 cert = ssl_sock.getpeercert()
#                 # print(cert)
#                 original_expiration_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
#                 expiration_date = original_expiration_date.strftime("%Y-%m-%d %H:%M:%S%z")
#                 remaining_days = (original_expiration_date - datetime.datetime.now()).days
#                 return url_input, expiration_date, remaining_days

#     except (ssl.SSLError, socket.gaierror) as e:
#         error_message = f"Error occurred: {str(e)}"
#         return None, error_message, None


import pytz
from django.utils import timezone

def get_ssl_certificate_info(url_input):
    url_input = url_input.lower()
    
    try:
        context = ssl.create_default_context()
        
        with socket.create_connection((url_input, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=url_input) as ssl_sock:
                cert = ssl_sock.getpeercert()
                original_expiration_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                tz_info = cert['notAfter'].split()[-1]
                tz = pytz.timezone(tz_info)
                expiration_date = original_expiration_date.replace(tzinfo=tz)
                remaining_days = (expiration_date - timezone.now()).days
                return url_input, expiration_date, remaining_days

    except (ssl.SSLError, socket.gaierror) as e:
        error_message = f"Error occurred: {str(e)}"
        return None, error_message, None