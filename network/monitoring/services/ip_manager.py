import subprocess
from netaddr import IPAddress
from monitoring.models import Device

class IPManager:
    @staticmethod
    def is_ip_available(ip_address):
        """Check if an IP is available (not in use)"""
        # Check database first
        if Device.objects.filter(ip_address=ip_address).exists():
            return False
            
        # Then check network with ARP ping
        try:
            # Try ARP ping (works on local network)
            result = subprocess.run(
                ['arping', '-c', '1', '-w', '1', ip_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return result.returncode != 0
        except:
            # Fallback to regular ping
            result = subprocess.run(
                ['ping', '-c', '1', '-W', '1', ip_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return result.returncode != 0
    
    @staticmethod
    def suggest_new_ip(network_range_id):
        """Suggest an available IP address from a range"""
        ip_range = IPRange.objects.get(id=network_range_id)
        available_ips = ip_range.get_available_ips()
        
        for ip in available_ips:
            if IPManager.is_ip_available(ip):
                return ip
        return None