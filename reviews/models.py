from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from bookings.models import Booking


class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}★ - {self.booking.listing.title}"

    def clean(self):
        if self.booking.status != 'completed':
            raise ValidationError("Reviews can only be left for completed bookings.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
