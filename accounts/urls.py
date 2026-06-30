from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/provider/', views.provider_dashboard, name='provider_dashboard'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
