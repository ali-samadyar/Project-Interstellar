from django.urls import path, include
from django.urls import reverse  
from . import views

# app_name = 'controlTower'

urlpatterns = [
    path('', views.management_func, name='management_func'),
    path('save_smtp_configuration/', views.save_smtp_configuration, name='save_smtp_configuration'),
    path('delete_smtp_configuration/', views.delete_smtp_configuration, name='delete_smtp_configuration'),
    path('get_smtp_configurations/', views.get_smtp_configurations, name='get_smtp_configurations'),
]
