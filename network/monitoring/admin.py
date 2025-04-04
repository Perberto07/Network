from django.contrib import admin
from .models import Device, IPRange

# Register your models here.
admin.site.register(Device)
admin.site.register(IPRange)