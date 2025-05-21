from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet, basename='booking-api')

#app_name = 'reservations'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.booking_list, name='booking-list'),
    path('booking/<int:pk>/', views.booking_detail, name='booking-detail'),
    path('create-booking/<int:hotel_id>/', views.create_booking, name='create-booking'),
    path('booking/<int:pk>/update/', views.booking_update, name='booking-update'),
    path('booking/<int:pk>/delete/', views.booking_delete, name='booking-delete'),
    path('booking/<int:pk>/cancel/', views.booking_cancel, name='booking-cancel'),
    
    # URLs pour les paiements
    path('payment/<int:booking_id>/create/', views.payment_create, name='payment-create'),
    path('payment/<int:pk>/', views.payment_detail, name='payment-detail'),
]