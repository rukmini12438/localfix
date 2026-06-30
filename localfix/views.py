from django.shortcuts import render
from listings.models import ServiceCategory, ServiceListing
from bookings.models import Booking


def home(request):
    categories = ServiceCategory.objects.all()[:6]
    listings = ServiceListing.objects.filter(is_active=True).select_related('provider', 'category')[:6]
    recent_bookings = []
    if request.user.is_authenticated:
        recent_bookings = Booking.objects.filter(customer=request.user).select_related('listing')[:3]
    return render(request, 'home.html', {
        'categories': categories,
        'listings': listings,
        'recent_bookings': recent_bookings,
    })
