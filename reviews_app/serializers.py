from rest_framework import serializers
from .models import Review
from hotel_app.serializers import HotelSerializer
from users_app.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    hotel = HotelSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'