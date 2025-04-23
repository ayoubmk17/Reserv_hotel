from rest_framework import serializers
from .models import Hotel, RoomType, Room
from users_app.serializers import UserSerializer

class HotelSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer(read_only=True)
    
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    hotel = HotelSerializer(read_only=True)
    
    class Meta:
        model = Room
        fields = '__all__'