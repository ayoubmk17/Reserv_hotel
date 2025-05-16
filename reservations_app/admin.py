from django.contrib import admin
from .models import Booking, Payment

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in', 'check_out', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'check_in', 'check_out')
    search_fields = ('user__username', 'room__room_number', 'special_requests')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_method', 'payment_date', 'is_successful')
    list_filter = ('payment_method', 'is_successful', 'payment_date')
    search_fields = ('transaction_id', 'booking__user__username')
    readonly_fields = ('payment_date',)
    list_per_page = 20
    date_hierarchy = 'payment_date'
    ordering = ('-payment_date',)
