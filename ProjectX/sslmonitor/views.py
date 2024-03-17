from django.views.generic import TemplateView
from .sslchecker import get_ssl_certificate_info
from django.shortcuts import redirect, render
from .models import SSLCertificate
from django.http import JsonResponse
from .models import EmailConfig
from controlTower.models import SMTPConfiguration
import datetime
import smtplib
from email.message import EmailMessage
import ssl



# Create your views here.


def sslchecker_function(request):
    context = {}

    if request.method == 'POST':
        if 'ssl_checker' in request.POST:

            url_input = request.POST.get('url_Input')
            processed_remaining_days = get_ssl_certificate_info(url_input)

            if processed_remaining_days is not None:
                # Display result in 'result_output'
                context = {'domain': processed_remaining_days[0],'remaining_days': processed_remaining_days[2], 'expiration_date': processed_remaining_days[1]}
                domain = processed_remaining_days[0]
                expiration_date = processed_remaining_days[1]
                remaining_days = processed_remaining_days[2]

                # Add result to the database
                if not SSLCertificate.objects.filter(domain=domain).exists():
                    SSLCertificate.objects.create(domain=domain, expiration_date=expiration_date, remaining_days=remaining_days)
                else:
                    SSLCertificate.objects.filter(domain=domain).update(expiration_date=expiration_date, remaining_days=remaining_days)
            else:
                # Display error message in 'result_output'
                context = {'error_message': 'Invalid URL'}
                
    else:
        # Code for Update SSL Certificates button
        ssl_certificates = SSLCertificate.objects.all()

        for ssl_certificate in ssl_certificates:
            url_input = ssl_certificate.domain
            processed_remaining_days = get_ssl_certificate_info(url_input)
            if processed_remaining_days is not None:
                ssl_certificate.expiration_date = processed_remaining_days[1]
                ssl_certificate.remaining_days = processed_remaining_days[2]
                ssl_certificate.save()

    # Fetch data from the database for table display
    ssl_certificates = SSLCertificate.objects.all()
    context['ssl_certificates'] = ssl_certificates

    # Fetch email configuration from the database
    email_configs = SMTPConfiguration.objects.all()  
    context['email_configs'] = email_configs

    return render(request, 'sslmonitor.html', context)

def remove_ssl_certificate(request):
    if request.method == 'POST':
        domain_to_remove = request.POST.get('domain')
        SSLCertificate.objects.filter(domain=domain_to_remove).delete()

    # Redirect to the original page or another appropriate page
    return redirect('sslchecker_function')

def save_email_config(request):
    if request.method == 'POST':
        smtp_name = request.POST.get('smtp_name')
        receiver = request.POST.get('receiver')

        try:
            # Ensure only one row in EmailConfig
            email_config, _ = EmailConfig.objects.get_or_create(pk=1)

            # Update the existing configuration with new values
            email_config.smtp_name = smtp_name
            email_config.receiver = receiver
            email_config.save()

            return JsonResponse({'success': True, 'message': 'Email configuration saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

def get_email_config(request):
    email_config = EmailConfig.objects.first()
    if email_config:
        return JsonResponse({'smtp_name': email_config.smtp_name, 'receiver': email_config.receiver})
    else:
        return JsonResponse({'error': 'No email configuration found'}, status=404)
    
    
def test_email(request):
    domains = SSLCertificate.objects.all()
    email_sent = False  # Flag to track if any email was sent
    for domain in domains:
        remaining_days = domain.remaining_days
        if remaining_days in [35, 40, 56]:
            email_config = EmailConfig.objects.first()  # Assuming there's only one email configuration
            smtp_config = SMTPConfiguration.objects.get(smtp_name=email_config.smtp_name)
            try:
                # Send email
                em = EmailMessage()
                em.set_content(f'SSL certificate of {domain.domain} will expire in {remaining_days} days. Please renew it.')
                em['Subject'] = f'{domain.domain} SSL Certificate Expiry Alert - {remaining_days} days remaining'
                em['From'] = smtp_config.smtp_sender
                em['To'] = email_config.receiver
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_config.smtp_server, smtp_config.smtp_server_port, context=context) as server:
                    server.login(smtp_config.smtp_sender, smtp_config.smtp_password)
                    server.send_message(em)
                    email_sent = True  # Set flag to True if email was sent
            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)}, status=500)
    
    if email_sent:
        return JsonResponse({'message': 'Test email sent successfully'})
    else:
        return JsonResponse({'message': 'No email sent'})
