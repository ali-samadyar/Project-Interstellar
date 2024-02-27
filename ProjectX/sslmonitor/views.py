from django.views.generic import TemplateView
from .sslchecker import get_ssl_certificate_info
from django.shortcuts import redirect, render
from .models import SSLCertificate
from django.utils import timezone
# Create your views here.


def sslchecker_function(request):
    context = {}

    if request.method == 'POST':
        if 'ssl_checker' in request.POST:

            url_input = request.POST.get('url_Input')
            processed_remaining_days = get_ssl_certificate_info(url_input)
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
        elif 'update_ssl_db' in request.POST:
            # Code for Update SSL Certificates button
            ssl_certificates = SSLCertificate.objects.all()

            for ssl_certificate in ssl_certificates:
                url_input = ssl_certificate.domain
                _, expiration_date, remaining_days = get_ssl_certificate_info(url_input)

                # Remove timezone information from expiration date
                expiration_date = expiration_date[:19]
                # Update SSL certificate information in the database
                ssl_certificate.expiration_date = timezone.datetime.strptime(expiration_date, "%Y-%m-%d %H:%M:%S")
                ssl_certificate.remaining_days = remaining_days
                ssl_certificate.save()
            

    # Fetch data from the database for table display
    ssl_certificates = SSLCertificate.objects.all()
    context['ssl_certificates'] = ssl_certificates

    return render(request, 'sslmonitor.html', context)

def remove_ssl_certificate(request):
    if request.method == 'POST':
        domain_to_remove = request.POST.get('domain')
        SSLCertificate.objects.filter(domain=domain_to_remove).delete()

    # Redirect to the original page or another appropriate page
    return redirect('sslchecker_function')
