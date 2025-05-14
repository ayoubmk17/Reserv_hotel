from django import forms
from .models import Hotel, Room, RoomType

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'address', 'city', 'country', 'email', 'phone']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name', 'description', 'base_price', 'capacity', 'amenities']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'room_type', 'room_number', 'floor', 'is_available']
        widgets = {
            'is_available': forms.CheckboxInput(),
        }