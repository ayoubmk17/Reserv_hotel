from rest_framework import viewsets, permissions
from .models import Booking, Payment
from .serializers import BookingSerializer, PaymentSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from hotel_app.models import Hotel, RoomType, Room
from datetime import datetime, timedelta
from decimal import Decimal
from django.utils import timezone
from .forms import BookingForm, PaymentForm
from django.urls import reverse

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        return Payment.objects.filter(booking__user=self.request.user)

# Vues pour l'interface web
@login_required
def booking_list(request):
    if request.user.role == 1:  # Client
        bookings = Booking.objects.filter(user=request.user)
    elif request.user.role == 2:  # Hotelier
        bookings = Booking.objects.filter(room__hotel__owner=request.user)
    else:
        bookings = Booking.objects.none()
    
    return render(request, 'reservations_app/booking_list.html', {
        'bookings': bookings
    })

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    # Vérifier que l'utilisateur a le droit de voir cette réservation
    if not (request.user == booking.user or request.user == booking.room.hotel.owner):
        messages.error(request, "Vous n'avez pas la permission de voir cette réservation.")
        return redirect('reservations:booking-list')
    
    return render(request, 'reservations_app/booking_detail.html', {
        'booking': booking
    })

@login_required
def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, "Votre réservation a été créée avec succès.")
            return redirect('reservations:booking-detail', pk=booking.pk)
    else:
        form = BookingForm()
    
    return render(request, 'reservations_app/booking_form.html', {
        'form': form,
        'title': 'Nouvelle réservation'
    })

@login_required
def booking_update(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if not (request.user == booking.user or request.user == booking.room.hotel.owner):
        messages.error(request, "Vous n'avez pas la permission de modifier cette réservation.")
        return redirect('reservations:booking-list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "La réservation a été mise à jour avec succès.")
            return redirect('reservations:booking-detail', pk=booking.pk)
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'reservations_app/booking_form.html', {
        'form': form,
        'booking': booking,
        'title': 'Modifier la réservation'
    })

@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if not (request.user == booking.user or request.user == booking.room.hotel.owner):
        messages.error(request, "Vous n'avez pas la permission de supprimer cette réservation.")
        return redirect('reservations:booking-list')
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "La réservation a été supprimée avec succès.")
        return redirect('reservations:booking-list')
    
    return render(request, 'reservations_app/booking_confirm_delete.html', {
        'booking': booking
    })

@login_required
def booking_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if not (request.user == booking.user or request.user == booking.room.hotel.owner):
        messages.error(request, "Vous n'avez pas la permission d'annuler cette réservation.")
        return redirect('reservations:booking-list')
    
    booking.status = Booking.CANCELLED
    booking.save()
    messages.success(request, "La réservation a été annulée avec succès.")
    return redirect('reservations:booking-detail', pk=booking.pk)

@login_required
def payment_create(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.user != booking.user:
        messages.error(request, "Vous n'avez pas la permission d'effectuer ce paiement.")
        return redirect('reservations:booking-list')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()
            messages.success(request, "Le paiement a été effectué avec succès.")
            return redirect('reservations:booking-detail', pk=booking.pk)
    else:
        form = PaymentForm(initial={'amount': booking.total_price})
    
    return render(request, 'reservations_app/payment_form.html', {
        'form': form,
        'booking': booking
    })

@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if not (request.user == payment.booking.user or request.user == payment.booking.room.hotel.owner):
        messages.error(request, "Vous n'avez pas la permission de voir ce paiement.")
        return redirect('reservations:booking-list')
    
    return render(request, 'reservations_app/payment_detail.html', {
        'payment': payment
    })

@login_required
def create_booking(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    room_types = hotel.room_types.all()
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    if request.method == 'POST':
        room_type_id = request.POST.get('room_type')
        check_in = datetime.strptime(request.POST.get('check_in'), '%Y-%m-%d').date()
        check_out = datetime.strptime(request.POST.get('check_out'), '%Y-%m-%d').date()
        adults = int(request.POST.get('adults', 1))
        children = int(request.POST.get('children', 0))
        special_requests = request.POST.get('special_requests', '')

        room_type = get_object_or_404(RoomType, pk=room_type_id)
        
        # Calculate total price
        nights = (check_out - check_in).days
        total_price = room_type.base_price * nights

        # Find an available room
        available_room = Room.objects.filter(
            hotel=hotel,
            room_type=room_type,
            is_available=True
        ).first()

        if not available_room:
            messages.error(request, 'Désolé, aucune chambre de ce type n\'est disponible pour les dates sélectionnées.')
            return redirect('create-booking', hotel_id=hotel_id)

        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            room=available_room,
            check_in=check_in,
            check_out=check_out,
            adults=adults,
            children=children,
            special_requests=special_requests,
            total_price=total_price,
            status=Booking.PENDING
        )

        # Mark the room as unavailable
        available_room.is_available = False
        available_room.save()

        messages.success(request, 'Votre réservation a été créée avec succès! Vous recevrez bientôt une confirmation.')
        return redirect('reservations:booking-detail', pk=booking.pk)

    return render(request, 'reservations_app/create_booking.html', {
        'hotel': hotel,
        'room_types': room_types,
        'today': today,
        'tomorrow': tomorrow,
    })

@login_required
def fake_payment(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        # Simuler le paiement et changer le statut
        booking.status = 'payed'
        booking.save()
        messages.success(request, 'Paiement effectué avec succès !')
        return redirect('reservations:booking-list')
    return render(request, 'reservations_app/fake_payment.html', {'booking': booking})