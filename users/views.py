from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after signup
            return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Login View
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')
