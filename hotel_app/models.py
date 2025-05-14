from django.db import models
from users_app.models import User

class Hotel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class RoomType(models.Model):
    STANDARD = 'standard'
    DELUXE = 'deluxe'
    PRESIDENTIELLE = 'presidentielle'
    
    TYPE_CHOICES = (
        (STANDARD, 'Chambre Standard'),
        (DELUXE, 'Chambre Deluxe'),
        (PRESIDENTIELLE, 'Suite Présidentielle'),
    )
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    amenities = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.hotel.name}"

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    floor = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Room {self.room_number} ({self.room_type.name}) - {self.hotel.name}"