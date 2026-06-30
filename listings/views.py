from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from accounts.mixins import ProviderRequiredMixin
from .models import ServiceListing, ServiceCategory


class ListingListView(ListView):
    model = ServiceListing
    template_name = 'listings/listing_list.html'
    context_object_name = 'listings'
    paginate_by = 9

    def get_queryset(self):
        qs = ServiceListing.objects.filter(is_active=True).select_related('provider', 'category')
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(category__name__icontains=query) |
                Q(location__icontains=query)
            )
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = ServiceCategory.objects.all()
        return ctx


class ListingDetailView(DetailView):
    model = ServiceListing
    template_name = 'listings/listing_detail.html'
    context_object_name = 'listing'


class ListingCreateView(ProviderRequiredMixin, CreateView):
    model = ServiceListing
    fields = ['category', 'title', 'description', 'price_range', 'location', 'availability']
    template_name = 'listings/listing_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.provider = self.request.user
        messages.success(self.request, "Listing published!")
        return super().form_valid(form)


class ListingUpdateView(ProviderRequiredMixin, UpdateView):
    model = ServiceListing
    fields = ['category', 'title', 'description', 'price_range', 'location', 'availability', 'is_active']
    template_name = 'listings/listing_form.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return ServiceListing.objects.filter(provider=self.request.user)
