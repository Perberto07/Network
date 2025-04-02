from django.db import models

# Create your models here.
class Device(models.Model):
    user = models.CharField(max_length=30)
    IPaddress = models.GenericIPAddressField(
        verbose_name="IP Address",
        unique=True,
        primary_key='both')
    is_active= models.BooleanField(default=True)

    def __str__(self):
        return self.user
