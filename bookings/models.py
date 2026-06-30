from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from listings.models import ServiceListing


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    # Allowed state transitions — the booking "state machine"
    TRANSITIONS = {
        'pending': ['confirmed', 'cancelled'],
        'confirmed': ['completed', 'cancelled'],
        'completed': [],
        'cancelled': [],
    }

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings',
                                  limit_choices_to={'profile__role': 'customer'})
    listing = models.ForeignKey(ServiceListing, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True, help_text="Any special instructions")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.listing.title} - {self.customer.username} ({self.status})"

    def can_transition_to(self, new_status):
        return new_status in self.TRANSITIONS.get(self.status, [])

    def transition_to(self, new_status):
        if not self.can_transition_to(new_status):
            raise ValidationError(f"Cannot move booking from '{self.status}' to '{new_status}'.")
        self.status = new_status
        self.save()
