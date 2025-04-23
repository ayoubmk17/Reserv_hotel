from rest_framework import serializers
from .models import Promotion
from hotel_app.serializers import HotelSerializer, RoomTypeSerializer

class PromotionSerializer(serializers.ModelSerializer):
    hotels = HotelSerializer(many=True, read_only=True)
    room_types = RoomTypeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Promotion
        fields = '__all__'