from django.urls import path
from . import views

# app_name = 'sslmonitor'

urlpatterns = [
    path('', views.sslchecker_function, name='sslchecker_function'),
    path('remove_ssl_certificate/', views.remove_ssl_certificate, name='remove_ssl_certificate'),
    path('update_ssl_certificates/', views.sslchecker_function, name='update_ssl_certificates'),

]