from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = router.urls