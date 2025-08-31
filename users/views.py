from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from decimal import Decimal
from books.models import Book
# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user to DB
            login(request, user)  # Automatically log them in
            messages.success(request, "Signup successful! Welcome 👋")
            return redirect('dashboard')  # Redirect to dashboard
        else:
            # Helpful feedback if signup fails
            messages.error(request, f"Signup failed: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Login View
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        """Redirect to dashboard after login"""
        messages.success(self.request, "Login successful ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Show errors if login fails"""
        messages.error(self.request, "Invalid username or password ❌")
        return super().form_invalid(form)

# Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# Dashboard View
@login_required
def dashboard_view(request):
    user_tx = Transaction.objects.filter(user=request.user).order_by("-date")

    income = sum((t.amount for t in user_tx if t.transaction_type == "income"), Decimal("0"))
    expenses = sum((t.amount for t in user_tx if t.transaction_type == "expense"), Decimal("0"))
    balance = income - expenses

    # 🔹 Get books from your database (instead of Google API)
    books_data = Book.objects.all()[:5]  # limit to 5

    context = {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "recent_tx": user_tx[:5],
        "all_tx": user_tx,
        "books": books_data,   # pass Book queryset directly
    }
    return render(request, "users/dashboard.html", context)
