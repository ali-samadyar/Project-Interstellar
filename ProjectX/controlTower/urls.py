from django.urls import path, include
from . import views

app_name = 'controlTower'

urlpatterns = [
    path('', views.management_func, name='management_func'),
    path('save_smtp_configuration/', views.save_smtp_configuration, name='save_smtp_configuration'),

]
