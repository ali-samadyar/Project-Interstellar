from django.urls import path
from . import views

urlpatterns = [
    path('', views.subnet_calculator_function, name='subnet_calculator_function'),
]
