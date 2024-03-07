from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views
from configGuardian.views import config_guardian

# app_name = 'sslmonitor'

urlpatterns = [
    path('', RedirectView.as_view(url='interface-mng/')),
    path('interface-mng/', views.device_data, name='device_data'),
    path('interface-mng/device/<str:device_ip>/interface/', views.get_interface_info, name='get_interface_info'),
    path('interface-mng/device/<str:device_ip>/ping/', views.ping_device, name='ping_device'), 
    path('interface-mng/device/<str:device_ip>/interface/<path:encoded_interface_name>/<str:action>/', views.device_interface_action, name='device_interface_action'),
    path('vlan', views.vlan_manager, name='vlan_manager'),
    path('command-runner/', views.show_command_runner, name='show_command_runner'),
    path('write-job/', views.write_memory, name='write_memory'),
    path('config-guardian/<str:device_ip>/', include('configGuardian.urls')),
    
]