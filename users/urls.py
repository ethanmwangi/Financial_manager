from django.urls import path
from .views import signup_view, CustomLoginView, logout_view
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Simple dashboard view
def dashboard_view(request):
    return render(request, 'users/dashboard.html')

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', login_required(dashboard_view), name='dashboard'),
]
