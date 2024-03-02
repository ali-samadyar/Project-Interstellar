from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landingpage'),
    path('about/', views.about, name='about'),
]