from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import NetworkMonitor, IPManager
from .models import Device, IPRange
from django.shortcuts import render

@api_view(['GET'])
def device_status(request, device_id):
    device = Device.objects.get(id=device_id)
    monitor = NetworkMonitor()
    is_online = monitor.check_device(device)
    return Response({
        'status': 'online' if is_online else 'offline',
        'last_seen': device.last_seen
    })

@api_view(['GET'])
def available_ips(request, range_id):
    ip_range = IPRange.objects.get(id=range_id)
    available = []
    
    for ip in ip_range.get_available_ips()[:50]:  # Limit to 50 results
        if IPManager.is_ip_available(ip):
            available.append(ip)
    
    return Response({'available_ips': available})

def dashboard(request):
    return render(request, 'monitoring/dashboard.html')