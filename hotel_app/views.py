from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Room
from .forms import HotelForm, RoomForm  # Vous devrez créer ces formulaires

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel_app/hotel_list.html', {'hotels': hotels})

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    return render(request, 'hotel_app/hotel_detail.html', {'hotel': hotel})

def hotel_create(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hotel-list')
    else:
        form = HotelForm()
    return render(request, 'hotel_app/hotel_form.html', {'form': form})

def room_list(request):
    # Récupérer toutes les chambres avec leurs relations
    rooms = Room.objects.select_related('hotel', 'room_type').all()
    
    # Contexte pour le template
    context = {
        'rooms': rooms,
        'title': 'Liste des Chambres'
    }
    
    return render(request, 'hotel_app/room_list.html', context)

def room_detail(request, pk):
    """
    Affiche les détails d'une chambre spécifique
    Args:
        pk (int): Primary key (ID) de la chambre
    """
    # Récupère la chambre ou renvoie 404
    room = get_object_or_404(
        Room.objects.select_related('hotel', 'room_type'),
        pk=pk
    )
    
    # Contexte pour le template
    context = {
        'room': room,
        'title': f'Chambre {room.room_number}'
    }
    
    return render(request, 'hotel_app/room_detail.html', context)


def home(request):
    return render(request,'home.html')