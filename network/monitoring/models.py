from django.db import models
from django.core.validators import validate_ipv46_address
from django.contrib.auth.models import User


#this is for Device and their IP
class Device(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('unknown', 'Unknown'),
    ]
    
    name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=17, blank=True, null=True)
    ip_address = models.GenericIPAddressField(unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unknown')
    last_seen = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_reserved = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.ip_address})"
    
    class Meta:
        ordering = ['ip_address']


class IPRange(models.Model):
    network_address = models.GenericIPAddressField()
    subnet_mask = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.network_address}/{self.subnet_mask}"
    
    def get_available_ips(self):
        """Returns list of available IPs in this range"""
        from netaddr import IPNetwork
        network = IPNetwork(f"{self.network_address}/{self.subnet_mask}")
        used_ips = set(Device.objects.filter(
            ip_address__startswith=self.network_address.split('.')[0]
        ).values_list('ip_address', flat=True))
        
        available_ips = []
        for ip in network.iter_hosts():
            ip_str = str(ip)
            if ip_str not in used_ips:
                available_ips.append(ip_str)
        
        return available_ips