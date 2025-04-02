from django.db import models

# Create your models here.
class Device(models.Model):
    User = models.CharField(max_length=30)
    id = models.IntegerField(auto_created= True, primary_key=True)
    IPaddress = models.GenericIPAddressField(
        verbose_name="IP Address",
        unique=True,
        protocol='both',)
    is_active= models.BooleanField(default=True)

    def __str__(self):
        return self.User
