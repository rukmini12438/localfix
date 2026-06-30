from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect


class ProviderRequiredMixin(UserPassesTestMixin):
    """Allows access only to logged-in users with role='provider'."""

    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.is_provider

    def handle_no_permission(self):
        messages.error(self.request, "This page is only for service providers.")
        return redirect('home')


class CustomerRequiredMixin(UserPassesTestMixin):
    """Allows access only to logged-in users with role='customer'."""

    def test_func(self):
        return hasattr(self.request.user, 'profile') and self.request.user.profile.is_customer

    def handle_no_permission(self):
        messages.error(self.request, "This page is only for customers.")
        return redirect('home')
