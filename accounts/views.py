from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import SignUpForm, ProfileUpdateForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created! Please log in.")
        return response


@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.is_provider:
        return redirect('provider_dashboard')
    return redirect('customer_dashboard')


@login_required
def provider_dashboard(request):
    from listings.models import ServiceListing
    from bookings.models import Booking
    listings = ServiceListing.objects.filter(provider=request.user)
    bookings = Booking.objects.filter(listing__provider=request.user).select_related('listing', 'customer')[:10]
    return render(request, 'accounts/provider_dashboard.html', {'listings': listings, 'bookings': bookings})


@login_required
def customer_dashboard(request):
    from bookings.models import Booking
    bookings = Booking.objects.filter(customer=request.user).select_related('listing')[:10]
    return render(request, 'accounts/customer_dashboard.html', {'bookings': bookings})


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})
