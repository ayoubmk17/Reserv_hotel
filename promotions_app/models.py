from django.db import models
from hotel_app.models import Hotel, RoomType

class Promotion(models.Model):
    PERCENTAGE = 'percentage'
    FIXED = 'fixed'
    
    DISCOUNT_TYPE_CHOICES = (
        (PERCENTAGE, 'Percentage'),
        (FIXED, 'Fixed Amount'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    hotels = models.ManyToManyField(Hotel, blank=True)
    room_types = models.ManyToManyField(RoomType, blank=True)
    min_stay_days = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return self.name