from rest_framework import serializers
from .models import Booking, Payment
from hotel_app.serializers import RoomSerializer
from users_app.serializers import UserSerializer

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'