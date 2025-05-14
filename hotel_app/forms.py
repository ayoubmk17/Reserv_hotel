from django import forms
from .models import Hotel, Room, RoomType

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'description', 'address', 'city', 'country', 'email', 'phone', 'image', 'base_price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'base_price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['hotel', 'name', 'description', 'base_price', 'capacity', 'amenities']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
        }

class RoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'hotel' in self.data:
            try:
                hotel_id = int(self.data.get('hotel'))
                self.fields['room_type'].queryset = RoomType.objects.filter(hotel_id=hotel_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['room_type'].queryset = self.instance.hotel.room_types.all()
        else:
            self.fields['room_type'].queryset = RoomType.objects.none()

    class Meta:
        model = Room
        fields = ['hotel', 'room_type', 'room_number', 'floor', 'is_available']
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }