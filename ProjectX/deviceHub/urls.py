from django.urls import path
from . import views

urlpatterns = [
    path('', views.device_hub, name='devicehub'),
    path('add-device/', views.add_device, name='add_device'),
    path('search/', views.search, name='search'),
    path('device_list_all/', views.device_list_all, name='device_list_all'),
    path('device_list_all/<int:id>/', views.get_device_detail, name='get_device_detail'),
    path('edit_device/<int:id>/', views.edit_device, name='edit_device'),
    path('fetch_device/<int:id>/', views.fetch_device, name='fetch_device'),

]