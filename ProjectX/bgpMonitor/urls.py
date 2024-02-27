from django.urls import path
from . import views

# app_name = 'sslmonitor'

urlpatterns = [
    path('', views.bgp_checker, name='bgp_checker'),

]