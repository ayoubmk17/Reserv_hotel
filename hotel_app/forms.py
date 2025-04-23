from django import forms
from .models import Hotel, Room

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'address', 'city','phone','country']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'room_type', 'room_number']