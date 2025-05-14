from django.urls import path
from .views import *

urlpatterns = [
    # Hôtels
    path('', home,name='home'),
    path('hotels/', hotel_list, name='hotel-list'),
    path('hotels/<int:pk>/', hotel_detail, name='hotel-detail'),
    path('hotels/create/', hotel_create, name='hotel-create'),
    
    # Chambres
    path('rooms/', room_list, name='room-list'),
    path('rooms/<int:pk>/', room_detail, name='room-detail'),
]