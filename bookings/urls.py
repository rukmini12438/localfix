from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('book/<int:listing_id>/', views.create_booking, name='create_booking'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    path('<int:pk>/status/<str:new_status>/', views.update_booking_status, name='update_booking_status'),
]
