from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from decimal import Decimal
import requests
import json
from books.models import Book

# Signup View
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful! Welcome 👋")
            return redirect('dashboard')
        else:
            messages.error(request, f"Signup failed: {form.errors}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Login View
class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Login successful ✅")
        return super().form_valid(form)

    def form_invalid(self, form):
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
    print("🔍 DEBUG: Dashboard view started")
    
    # Calculate financial totals
    user_tx = Transaction.objects.filter(user=request.user).order_by("-date")
    income = sum((t.amount for t in user_tx if t.transaction_type == "INCOME"), Decimal("0"))
    expenses = sum((t.amount for t in user_tx if t.transaction_type == "EXPENSE"), Decimal("0"))
    balance = income - expenses
    print(f"💰 DEBUG: Balance calculated: ${balance}")

    # Get books directly from database (skip API call for now)
    from books.models import Book
    books_queryset = Book.objects.all()[:6]  # Get first 6 books
    
    # Convert to list of dictionaries (like API would return)
    books_data = []
    for book in books_queryset:
        books_data.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'description': book.description,
            'published_date': str(book.published_date) if book.published_date else None
        })
    
    print(f"📚 DEBUG: Got {len(books_data)} books from database")
    print(f"📖 DEBUG: First book: {books_data[0] if books_data else 'None'}")

    context = {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "recent_tx": user_tx[:5],
        "books": books_data,  # This should now have your 7 books (limited to 6)
    }
    
    print("🎯 DEBUG: Context created, rendering template")
    return render(request, "users/dashboard.html", context)