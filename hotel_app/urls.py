from django.urls import path
from .views import *

urlpatterns = [
    # Hôtels
    path('', home,name='home'),
    path('hotels/', hotel_list, name='hotel-list'),
    path('hotels/<int:pk>/', hotel_detail, name='hotel-detail'),
    path('hotels/create/', hotel_create, name='hotel-create'),
    path('hotels/<int:pk>/update/', hotel_update, name='hotel-update'),
    path('hotels/<int:pk>/delete/', hotel_delete, name='hotel-delete'),
    
    # Chambres
    path('rooms/', room_list, name='room-list'),
    path('rooms/create/', room_create, name='room-create'),
    path('rooms/<int:pk>/', room_detail, name='room-detail'),
    path('rooms/<int:pk>/delete/', room_delete, name='room-delete'),
    path('rooms/<int:pk>/toggle-availability/', toggle_room_availability, name='room-toggle-availability'),
    
    # Types de chambres
    path('room-types/', room_type_list, name='room-type-list'),
    path('room-types/create/', room_type_create, name='room-type-create'),
    path('room-types/<int:pk>/delete/', room_type_delete, name='room-type-delete'),
    
    # API
    path('api/room-types/<int:hotel_id>/', get_room_types, name='get-room-types'),
    path('contact/', contact, name='contact'),
]