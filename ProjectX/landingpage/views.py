from django.shortcuts import render

# Create your views here.

app_name = 'landingpage'

def landing(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'about.html')
