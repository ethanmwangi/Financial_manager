from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction  # keep this import
from decimal import Decimal

# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
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

#  Dashboard View 
@login_required
def dashboard_view(request):
    qs = Transaction.objects.filter(user=request.user)

    income = sum((t.amount for t in qs if t.transaction_type == 'income'), Decimal('0'))
    expenses = sum((t.amount for t in qs if t.transaction_type == 'expense'), Decimal('0'))
    balance = income - expenses

    context = {
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'recent_tx': qs.order_by('-date')[:5],  # last 5, used in the template
    }
    return render(request, 'users/dashboard.html', context)
