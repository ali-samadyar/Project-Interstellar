from django.urls import path
from django.views.generic.base import RedirectView
from . import views

# app_name = 'sslmonitor'

urlpatterns = [
    path('', RedirectView.as_view(url='interface-mng/')),
    path('interface-mng/', views.device_data, name='device_data'),
    path('/device/<str:device_ip>/interface/', views.get_interface_info, name='get_interface_info'),
    path('/device/<str:device_ip>/ping/', views.ping_device, name='ping_device'), 
    path('vlan', views.vlan_manager, name='vlan_manager'),
    
]