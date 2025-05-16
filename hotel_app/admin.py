from django.contrib import admin
from .models import Hotel, RoomType, Room

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'country', 'email', 'phone', 'base_price')
    list_filter = ('city', 'country')
    search_fields = ('name', 'description', 'address', 'city', 'country', 'owner__username')
    list_per_page = 20
    ordering = ('name',)

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'base_price', 'capacity')
    list_filter = ('name', 'hotel', 'capacity')
    search_fields = ('hotel__name', 'description', 'amenities')
    list_per_page = 20
    ordering = ('hotel', 'name')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hotel', 'room_type', 'floor', 'is_available')
    list_filter = ('hotel', 'room_type', 'floor', 'is_available')
    search_fields = ('room_number', 'hotel__name', 'room_type__name')
    list_per_page = 20
    ordering = ('hotel', 'room_number')
