from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hotel_app.models import Hotel
from reservations_app.models import Booking

# Create your views here.

@login_required
def profile_view(request):
    context = {
        'user': request.user
    }
    
    if request.user.role == 2:  # Hôtelier
        context['hotels'] = Hotel.objects.filter(owner=request.user)
    else:  # Client
        context['reservations'] = Booking.objects.filter(user=request.user)
    
    return render(request, 'profiles/profile.html', context)
