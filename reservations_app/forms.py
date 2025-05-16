from django import forms
from .models import Booking, Payment
from hotel_app.models import Room, Hotel

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out', 'adults', 'children', 'special_requests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
            'adults': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'children': forms.NumberInput(attrs={'min': 0, 'max': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ne montrer que les chambres disponibles
        self.fields['room'].queryset = Room.objects.filter(is_available=True)

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        room = cleaned_data.get('room')
        
        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError(
                    "La date de départ doit être postérieure à la date d'arrivée."
                )
            
            # Vérifier les conflits de réservation
            if room:
                conflicting_bookings = Booking.objects.filter(
                    room=room,
                    check_out__gt=check_in,
                    check_in__lt=check_out,
                    status__in=['pending', 'confirmed']
                ).exclude(pk=self.instance.pk if self.instance else None)
                
                if conflicting_bookings.exists():
                    raise forms.ValidationError(
                        "Cette chambre n'est pas disponible pour les dates sélectionnées."
                    )
        
        return cleaned_data

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'transaction_id']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        } 