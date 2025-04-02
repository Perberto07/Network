from django.urls import path
from . import views

app_name='Netmonitor'

urlpatterns = [
    path('dashboard/', views.dashboard , name='dashboard'),
]

