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

# Dashboard View - ULTIMATE DEBUG VERSION
@login_required
def dashboard_view(request):
    print("🚨 ULTIMATE DEBUG: This dashboard view is running!")
    
    # Calculate financial totals
    user_tx = Transaction.objects.filter(user=request.user).order_by("-date")
    income = sum((t.amount for t in user_tx if t.transaction_type == "income"), Decimal("0"))
    expenses = sum((t.amount for t in user_tx if t.transaction_type == "expense"), Decimal("0"))
    balance = income - expenses
    print(f"💰 Balance: ${balance}")

    # Import books model and test
    print("📚 Testing books import...")
    try:
        from books.models import Book
        print("✅ Books model imported successfully")
        
        book_count = Book.objects.count()
        print(f"📊 Book count in database: {book_count}")
        
        books_queryset = Book.objects.all()[:6]
        print(f"📋 Queryset length: {len(books_queryset)}")
        
        # Convert to list
        books_data = []
        for book in books_queryset:
            book_dict = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'description': book.description,
                'published_date': str(book.published_date) if book.published_date else None
            }
            books_data.append(book_dict)
            print(f"📖 Added book: {book.title}")
        
        print(f"📚 Final books_data length: {len(books_data)}")
        print(f"📝 First book data: {books_data[0] if books_data else 'NONE'}")
        
    except Exception as e:
        print(f"💥 Error with books: {e}")
        books_data = []

    # Test context creation
    context = {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "recent_tx": user_tx[:5],
        "books": books_data,
    }
    
    print(f"🎯 Context books length: {len(context['books'])}")
    print(f"🎯 Context keys: {list(context.keys())}")
    
    print("🎨 About to render template...")
    return render(request, "users/dashboard.html", context)

