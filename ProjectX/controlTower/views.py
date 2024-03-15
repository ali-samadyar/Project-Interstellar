from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import SMTPConfigurationForm
from .models import SMTPConfiguration
from django.core import serializers


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
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
    

def delete_smtp_configuration(request):
    if request.method == 'POST':
        smtp_id = request.POST.get('id')
        SMTPConfiguration.objects.filter(id=smtp_id).delete()
    return redirect('management_func')
        

def get_smtp_configurations(request):
    smtp_configurations = SMTPConfiguration.objects.all()
    data = serializers.serialize('json', smtp_configurations)
    print(data)
    return JsonResponse({'success': True, 'smtp_configurations': data})
