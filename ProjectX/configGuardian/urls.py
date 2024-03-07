from django.urls import path
from . import views

urlpatterns = [
    path('', views.config_guardian, name='config_guardian'),
    path('<str:device_ip>/', views.config_guardian, name='config_guardian_with_ip'),
    path('remove/<int:backup_id>/', views.remove_backup, name='remove_backup'),

]