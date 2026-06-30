from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('listing', 'customer', 'date', 'time', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('listing__title', 'customer__username')
