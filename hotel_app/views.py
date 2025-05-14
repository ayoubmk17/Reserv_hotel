from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Min
from .models import Hotel, Room, RoomType
from .forms import HotelForm, RoomForm

def home(request):
    # Récupérer les hôtels avec leur prix minimum
    hotels = Hotel.objects.annotate(
        min_price=Min('room_types__base_price')
    ).order_by('-min_price')[:6]  # Limiter à 6 hôtels populaires
    
    return render(request, 'home.html', {'hotels': hotels})

def hotel_list(request):
    hotels = Hotel.objects.all()
    city = request.GET.get('city')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    
    if city:
        hotels = hotels.filter(city__icontains=city)
    
    # Ajouter le prix minimum pour chaque hôtel
    hotels = hotels.annotate(min_price=Min('room_types__base_price'))
    
    context = {
        'hotels': hotels,
        'city': city,
        'check_in': check_in,
        'check_out': check_out,
    }
    return render(request, 'hotel_app/hotel_list.html', context)

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    room_types = hotel.room_types.all()
    return render(request, 'hotel_app/hotel_detail.html', {
        'hotel': hotel,
        'room_types': room_types
    })

@login_required
def hotel_create(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            return redirect('hotel-list')
    else:
        form = HotelForm()
    return render(request, 'hotel_app/hotel_form.html', {'form': form})

def room_list(request):
    rooms = Room.objects.select_related('hotel', 'room_type').all()
    context = {
        'rooms': rooms,
        'title': 'Liste des Chambres'
    }
    return render(request, 'hotel_app/room_list.html', context)

def room_detail(request, pk):
    room = get_object_or_404(
        Room.objects.select_related('hotel', 'room_type'),
        pk=pk
    )
    context = {
        'room': room,
        'title': f'Chambre {room.room_number}'
    }
    return render(request, 'hotel_app/room_detail.html', context)

@login_required
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            # Vérifier que l'utilisateur est propriétaire de l'hôtel
            if room.hotel.owner != request.user:
                return redirect('hotel-list')
            room.save()
            return redirect('room-list')
    else:
        form = RoomForm()
        # Filtrer les hôtels pour n'afficher que ceux de l'utilisateur
        form.fields['hotel'].queryset = Hotel.objects.filter(owner=request.user)
    return render(request, 'hotel_app/room_form.html', {'form': form})