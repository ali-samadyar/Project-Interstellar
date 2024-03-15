from django.shortcuts import render
from django.http import JsonResponse
from .forms import SMTPConfigurationForm
from .models import SMTPConfiguration


# Create your views here.

def management_func(request):
    smtp_db_data = SMTPConfiguration.objects.all()
    return render(request, 'control_tower.html', {'smtp_db_data': smtp_db_data})


def save_smtp_configuration(request):
    if request.method == 'POST':
        form = SMTPConfigurationForm(request.POST)
        if form.is_valid():
            smtp_config = form.save()
            return JsonResponse({'success': True, 'message': 'SMTP configuration saved successfully'})
        else:
            errors = form.errors.as_json()
            print(errors)
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)