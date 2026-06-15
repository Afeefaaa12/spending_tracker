from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/view/', views.view_transactions, name='view_transactions'),
    path('categories/add/', views.add_category, name='add_category'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('transactions/edit/<int:id>/', views.edit_transaction, name='edit_transaction'),
    path('transactions/delete/<int:id>/', views.delete_transaction, name='delete_transaction'),
   path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout')

 
]