from django.contrib import admin
from .models import ServiceCategory, ServiceListing

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ServiceListing)
class ServiceListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'category', 'location', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'location', 'provider__username')
