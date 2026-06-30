from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from accounts.mixins import CustomerRequiredMixin, ProviderRequiredMixin
from listings.models import ServiceListing
from .models import Booking
from .forms import BookingForm


@login_required
def create_booking(request, listing_id):
    listing = get_object_or_404(ServiceListing, pk=listing_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.listing = listing
            booking.save()
            messages.success(request, "Booking request sent!")
            send_mail(
                'New booking request',
                f'{request.user.username} requested a booking for {listing.title}.',
                'noreply@localfix.com',
                [listing.provider.email],
                fail_silently=True,
            )
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {'form': form, 'listing': listing})


@login_required
def booking_list(request):
    if request.user.profile.is_provider:
        bookings = Booking.objects.filter(listing__provider=request.user).select_related('listing', 'customer')
    else:
        bookings = Booking.objects.filter(customer=request.user).select_related('listing')
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def update_booking_status(request, pk, new_status):
    booking = get_object_or_404(Booking, pk=pk, listing__provider=request.user)
    try:
        booking.transition_to(new_status)
        messages.success(request, f"Booking marked as {new_status}.")
    except Exception as e:
        messages.error(request, str(e))
    return redirect('booking_list')
