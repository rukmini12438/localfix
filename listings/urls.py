from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListingListView.as_view(), name='listing_list'),
    path('new/', views.ListingCreateView.as_view(), name='listing_create'),
    path('<int:pk>/', views.ListingDetailView.as_view(), name='listing_detail'),
    path('<int:pk>/edit/', views.ListingUpdateView.as_view(), name='listing_update'),
]
