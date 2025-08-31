from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from decimal import Decimal

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
# Dashboard View
@login_required
def dashboard_view(request):
    # Always filter by username instead of direct user object
    user_tx = Transaction.objects.filter(user__username=request.user.username)

    # Debugging
    all_tx = Transaction.objects.all()
    print("DEBUG: Logged-in user:", request.user)
    print("DEBUG: All transactions in DB:", list(all_tx))
    print("DEBUG: Transactions for this user (by username):", list(user_tx))

    income = sum((t.amount for t in user_tx if str(t.transaction_type).lower() == 'income'), Decimal('0'))
    expenses = sum((t.amount for t in user_tx if str(t.transaction_type).lower() == 'expense'), Decimal('0'))
    balance = income - expenses

    context = {
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'recent_tx': user_tx.order_by('-date')[:5],  # ✅ use username-filtered qs
        'all_tx': all_tx,
        'user_tx': user_tx
    }
    return render(request, 'users/dashboard.html', context)

# --- New: Fetch Books from Google Books API ---
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": "financial literacy", "maxResults": 5}
    books_data = []
    try:
        res = requests.get(url, params=params, timeout=5)
        res.raise_for_status()
        data = res.json()

        for item in data.get("items", []):
            volume = item["volumeInfo"]
            books_data.append({
                "title": volume.get("title"),
                "authors": ", ".join(volume.get("authors", ["Unknown"])),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail"),
                "previewLink": volume.get("previewLink"),
            })
    except Exception as e:
        print("Google Books API error:", e)

    context = {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "recent_tx": qs.order_by("-date")[:5],
        "books": books_data,  # ✅ pass books to template
    }
    return render(request, "users/dashboard.html", context)