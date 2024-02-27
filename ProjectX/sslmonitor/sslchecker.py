import ssl
import socket
import datetime

# Function to get SSL certificate information for a given URL
def get_ssl_certificate_info(url_input):
    url_input = url_input.lower()
    
    try:
        # Creating a default SSL context
        context = ssl.create_default_context()
        
        # Creating a socket connection to the URL on port 443 (HTTPS)
        with socket.create_connection((url_input, 443)) as sock:
            # Wrapping the socket with SSL/TLS
            with context.wrap_socket(sock, server_hostname=url_input) as ssl_sock:
                # Getting the peer certificate
                cert = ssl_sock.getpeercert()
                
                # Parsing the expiration date from the certificate
                original_expiration_date = datetime.datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                
                # Formatting the expiration date (the django db will not accept the original format)
                expiration_date = original_expiration_date.strftime("%Y-%m-%d %H:%M:%S%z")

                # Calculating the remaining days until expiration
                remaining_days = (original_expiration_date - datetime.datetime.now()).days

                # print(url_input, expiration_date, issued_by, remaining_days)

                # Returning the URL, formatted expiration date, issued by, and remaining days
                return url_input, expiration_date, remaining_days

    # Handling SSL errors
    except ssl.SSLError:
        return None
    
    # Handling socket errors
    except socket.gaierror:
        return None
