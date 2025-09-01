# transactions/views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@login_required
def transaction_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    if query:
        transactions = transactions.filter(description__icontains=query)
    if category and category != 'all':
        transactions = transactions.filter(category=category)
    if start_date:
        transactions = transactions.filter(date__gte=start_date)
    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    income = sum((t.amount for t in transactions if t.transaction_type == 'income'), Decimal('0'))
    expenses = sum((t.amount for t in transactions if t.transaction_type == 'expense'), Decimal('0'))
    balance = income - expenses

    # If you have CATEGORY_CHOICES in your model:
    categories = [c[0] for c in getattr(Transaction, 'CATEGORY_CHOICES', [])]

    return render(request, 'transactions/transaction_list.html', {
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'query': query,
        'category': category,
        'categories': categories,
        'start_date': start_date,
        'end_date': end_date,
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_breakdown_api(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user, transaction_type='expense')
    categories = {}
    for tx in transactions:
        cat = tx.category if tx.category else "Other"
        categories[cat] = categories.get(cat, 0) + float(tx.amount)
    return Response({
        "categories": list(categories.keys()),
        "amounts": list(categories.values())
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def income_breakdown_api(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user, transaction_type='income')
    categories = {}
    for tx in transactions:
        cat = tx.category if tx.category else "Other"
        categories[cat] = categories.get(cat, 0) + float(tx.amount)
    return Response({
        "categories": list(categories.keys()),
        "amounts": list(categories.values())
    })