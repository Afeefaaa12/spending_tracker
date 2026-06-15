from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm, RegisterForm

from collections import defaultdict

@login_required
def dashboard(request):
    income = Transaction.objects.filter(user=request.user, category__type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense = Transaction.objects.filter(user=request.user, category__type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = income - expense
    return render(request, 'dashboard.html', {'income': income, 'expense': expense, 'balance': balance})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('view_transactions')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'add_transaction.html', {'form': form})

@login_required
def view_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'view_transactions.html', {'transactions': transactions})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('add_category')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

@login_required
def reports(request):
    transactions = Transaction.objects.filter(user=request.user, category__type='expense')
    data = defaultdict(float)
    for t in transactions:
        data[t.category.name] += t.amount
    labels = list(data.keys())
    values = list(data.values())
    return render(request, 'reports.html', {'labels': labels, 'values': values})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

@login_required
def edit_transaction(request, id):
    transaction = Transaction.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_transactions')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(request, 'add_transaction.html', {'form': form, 'edit': True})


@login_required
def delete_transaction(request, id):
    transaction = Transaction.objects.get(id=id, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('view_transactions')
    return render(request, 'confirm_delete.html', {'transaction': transaction})

def logout_view(request):
    logout(request)
    return redirect('login')
