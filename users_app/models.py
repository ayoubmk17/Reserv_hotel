from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CLIENT = 1
    HOTELIER = 2
    ADMIN = 3
    
    ROLE_CHOICES = (
        (CLIENT, 'Client'),
        (HOTELIER, 'Hotelier'),
        (ADMIN, 'Admin'),
    )
    
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CLIENT)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"