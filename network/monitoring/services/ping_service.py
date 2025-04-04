from pythonping import ping
from datetime import datetime
import threading
from concurrent.futures import ThreadPoolExecutor
from monitoring.models import Device

class NetworkMonitor:
    def __init__(self, timeout=1, count=2):
        self.timeout = timeout
        self.count = count
        
    def check_device(self, device):
        try:
            response = ping(
                device.ip_address,
                count=self.count,
                timeout=self.timeout,
                verbose=False
            )
            
            is_online = response.success()
            device.status = 'online' if is_online else 'offline'
            if is_online:
                device.last_seen = datetime.now()
            device.save()
            return is_online
            
        except Exception as e:
            device.status = 'unknown'
            device.save()
            return False
    
    def scan_network(self, network_devices):
        """Scan multiple devices in parallel"""
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(self.check_device, network_devices))
        return results