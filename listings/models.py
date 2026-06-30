from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Avg


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, default='fa-screwdriver-wrench',
                             help_text="Font Awesome class e.g. fa-bolt")
    color = models.CharField(max_length=20, blank=True, default='#4F46E5',
                              help_text="Hex color for the icon badge")

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class ServiceListing(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings',
                                  limit_choices_to={'profile__role': 'provider'})
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_range = models.CharField(max_length=100, help_text="e.g. ₹500 - ₹1500")
    location = models.CharField(max_length=255)
    availability = models.CharField(max_length=255, help_text="e.g. Mon-Sat, 9am-6pm")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.provider.username}"

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'pk': self.pk})

    @property
    def average_rating(self):
        from reviews.models import Review
        result = Review.objects.filter(booking__listing=self).aggregate(avg=Avg('rating'))
        return round(result['avg'], 1) if result['avg'] else None

    @property
    def review_count(self):
        from reviews.models import Review
        return Review.objects.filter(booking__listing=self).count()
