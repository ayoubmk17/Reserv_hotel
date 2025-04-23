from django.db import models
from users_app.models import User
from hotel_app.models import Hotel
from reservations_app.models import Booking

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    cleanliness = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    service = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comfort = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    location = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.hotel.name}"