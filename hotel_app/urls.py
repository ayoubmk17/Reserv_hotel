from django.urls import path
from . import views

urlpatterns = [
    # Hôtels
    path('hotels/', views.hotel_list, name='hotel-list'),
    path('hotels/<int:pk>/', views.hotel_detail, name='hotel-detail'),
    path('hotels/create/', views.hotel_create, name='hotel-create'),
    
    # Chambres
    path('rooms/', views.room_list, name='room-list'),
    path('rooms/<int:pk>/', views.room_detail, name='room-detail'),
]