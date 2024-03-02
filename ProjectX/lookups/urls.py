from django.urls import path
from . import views

urlpatterns = [
    path('', views.lookups, name='lookups'),
]
