from django.urls import path
from . import views

# app_name = 'sslmonitor'

urlpatterns = [
    path('', views.sslchecker_function, name='sslchecker_function'),
    path('remove_ssl_certificate/', views.remove_ssl_certificate, name='remove_ssl_certificate'),
    path('save_email_config/', views.save_email_config, name='save_email_config'),
    path('test_email/', views.test_email, name='test_email'),
    path('get_email_config/', views.get_email_config, name='get_email_config'),

    # path('update_ssl_certificates/', views.sslchecker_function, name='update_ssl_certificates'),

]