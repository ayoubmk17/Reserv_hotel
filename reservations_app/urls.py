from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet, basename='booking-api')

urlpatterns = [
    path('api/', include(router.urls)),
    path('booking/<int:pk>/', views.booking_detail, name='booking-detail'),
    path('create-booking/<int:hotel_id>/', views.create_booking, name='create-booking'),
]