from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

# Import Transaction model
from transactions.models import Transaction


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


@login_required
def dashboard_view(request):
    # Fetch user-specific transactions
    transactions = Transaction.objects.filter(user=request.user)

    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    balance = total_income - total_expenses

    context = {
        "transactions": transactions.order_by('-date')[:5],  # last 5
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
    }
    return render(request, 'users/dashboard.html', context)
