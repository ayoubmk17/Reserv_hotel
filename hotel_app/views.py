from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Min
from .models import Hotel, Room, RoomType
from .forms import HotelForm, RoomForm, RoomTypeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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
        'user_role': request.user.role if request.user.is_authenticated else None,
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
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.owner = request.user
            hotel.save()
            return redirect('hotel-list')
    else:
        form = HotelForm()
    return render(request, 'hotel_app/hotel_form.html', {'form': form})

@login_required
def hotel_update(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    
    # Vérifier que l'utilisateur est le propriétaire
    if hotel.owner != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cet hôtel.")
        return redirect('hotel-list')
    
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, "L'hôtel a été modifié avec succès.")
            return redirect('hotel-list')
    else:
        form = HotelForm(instance=hotel)
    
    return render(request, 'hotel_app/hotel_form.html', {
        'form': form,
        'hotel': hotel,
        'is_update': True
    })

@login_required
def hotel_delete(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    
    # Vérifier que l'utilisateur est le propriétaire
    if hotel.owner != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cet hôtel.")
        return redirect('hotel-list')
    
    if request.method == 'POST':
        hotel.delete()
        messages.success(request, "L'hôtel a été supprimé avec succès.")
        return redirect('hotel-list')
    
    return render(request, 'hotel_app/hotel_confirm_delete.html', {'hotel': hotel})

def room_list(request):
    rooms = Room.objects.select_related('hotel', 'room_type').all()
    hotels = Hotel.objects.all()
    
    if request.user.is_authenticated and request.user.role == 2:
        # Si c'est un propriétaire, ne montrer que ses chambres
        rooms = rooms.filter(hotel__owner=request.user)
        hotels = hotels.filter(owner=request.user)
    
    context = {
        'rooms': rooms,
        'hotels': hotels,
        'title': 'Gestion des Chambres'
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
                messages.error(request, "Vous n'avez pas la permission d'ajouter une chambre à cet hôtel.")
                return redirect('room-list')
            room.save()
            messages.success(request, "La chambre a été créée avec succès.")
            return redirect('room-list')
    else:
        form = RoomForm()
        # Filtrer les hôtels pour n'afficher que ceux de l'utilisateur
        user_hotels = Hotel.objects.filter(owner=request.user)
        form.fields['hotel'].queryset = user_hotels
        
        # Vérifier si l'utilisateur a des types de chambres
        has_room_types = RoomType.objects.filter(hotel__owner=request.user).exists()
        if not has_room_types and user_hotels.exists():
            messages.warning(request, "Vous devez d'abord créer des types de chambres avant de pouvoir ajouter des chambres.")
            return redirect('room-type-create')
        
    return render(request, 'hotel_app/room_form.html', {'form': form})

@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    
    # Vérifier que l'utilisateur est le propriétaire de l'hôtel
    if room.hotel.owner != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette chambre.")
        return redirect('room-list')
    
    if request.method == 'POST':
        room.delete()
        messages.success(request, "La chambre a été supprimée avec succès.")
        return redirect('room-list')
    
    return render(request, 'hotel_app/room_confirm_delete.html', {'room': room})

@login_required
def room_type_create(request):
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            room_type = form.save(commit=False)
            # Vérifier que l'utilisateur est propriétaire de l'hôtel
            if room_type.hotel.owner != request.user:
                messages.error(request, "Vous n'avez pas la permission d'ajouter un type de chambre à cet hôtel.")
                return redirect('room-type-list')
            room_type.save()
            messages.success(request, "Le type de chambre a été créé avec succès.")
            
            # Si l'utilisateur vient de la création de chambre, le rediriger vers la création de chambre
            if request.GET.get('next') == 'room_create':
                return redirect('room-create')
            return redirect('room-type-list')
    else:
        form = RoomTypeForm()
        # Filtrer les hôtels pour n'afficher que ceux de l'utilisateur
        user_hotels = Hotel.objects.filter(owner=request.user)
        if not user_hotels.exists():
            messages.error(request, "Vous devez d'abord créer un hôtel avant de pouvoir ajouter des types de chambres.")
            return redirect('hotel-create')
        form.fields['hotel'].queryset = user_hotels
        
        # Si un seul hôtel, le sélectionner par défaut
        if user_hotels.count() == 1:
            form.fields['hotel'].initial = user_hotels.first()
    
    return render(request, 'hotel_app/room_type_form.html', {'form': form})

@login_required
def room_type_list(request):
    # Récupérer uniquement les types de chambres des hôtels de l'utilisateur
    room_types = RoomType.objects.filter(hotel__owner=request.user)
    return render(request, 'hotel_app/room_type_list.html', {'room_types': room_types})

@login_required
def room_type_delete(request, pk):
    room_type = get_object_or_404(RoomType, pk=pk)
    
    # Vérifier que l'utilisateur est le propriétaire de l'hôtel
    if room_type.hotel.owner != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce type de chambre.")
        return redirect('room-type-list')
    
    if request.method == 'POST':
        room_type.delete()
        messages.success(request, "Le type de chambre a été supprimé avec succès.")
        return redirect('room-type-list')
    
    return render(request, 'hotel_app/room_type_confirm_delete.html', {'room_type': room_type})

@login_required
def get_room_types(request, hotel_id):
    room_types = []
    for room_type in RoomType.objects.filter(hotel_id=hotel_id):
        room_types.append({
            'id': room_type.id,
            'name': room_type.get_name_display()  # Utiliser get_name_display() pour obtenir le nom lisible
        })
    return JsonResponse(room_types, safe=False)

@login_required
@require_POST
def toggle_room_availability(request, pk):
    room = get_object_or_404(Room, pk=pk)
    
    # Vérifier que l'utilisateur est le propriétaire de l'hôtel
    if room.hotel.owner != request.user:
        return JsonResponse({
            'error': "Vous n'avez pas la permission de modifier cette chambre."
        }, status=403)
    
    # Inverser la disponibilité
    room.is_available = not room.is_available
    room.save()
    
    return JsonResponse({
        'is_available': room.is_available
    })

def contact(request):
    return render(request, 'contact.html')