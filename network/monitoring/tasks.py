from celery import shared_task
from .services import NetworkMonitor
from .models import Device
from datetime import datetime, timedelta

@shared_task
def monitor_all_devices():
    devices = Device.objects.filter(is_reserved=False)
    monitor = NetworkMonitor()
    monitor.scan_network(devices)

@shared_task
def check_ip_conflicts():
    """Check for IP conflicts in the network"""
    from .services import IPManager
    from .models import Device
    
    devices = Device.objects.all()
    conflict_devices = []
    
    for device in devices:
        if not IPManager.is_ip_available(device.ip_address):
            # If IP responds but isn't our device (by MAC)
            conflict_devices.append(device)
    
    return conflict_devices