from django.urls import path
from . import views

app_name='monitoring'

urlpatterns = [
    path('dashboard/', views.dashboard , name='dashboard'),
    path('device/<int:device_id>/status/', views.device_status),
    path('ip-range/<int:range_id>/available-ips/', views.available_ips),
]

