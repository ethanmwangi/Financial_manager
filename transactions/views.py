# transactions/views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm

@login_required
def transaction_list(request):
    query = request.GET.get('q')
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    if query:
        transactions = transactions.filter(description__icontains=query)

    # Totals (calculated from ALL of the user’s transactions, not just search results)
    user_tx = Transaction.objects.filter(user=request.user)
    income = sum((t.amount for t in user_tx if t.transaction_type == 'income'), Decimal('0'))
    expenses = sum((t.amount for t in user_tx if t.transaction_type == 'expense'), Decimal('0'))
    balance = income - expenses

    return render(request, 'transactions/transaction_list.html', {
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'query': query,
    })


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/transaction_form.html', {'form': form})


@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/edit_transaction.html', {'form': form})


@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transactions/delete_transaction.html', {'transaction': transaction})


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})
