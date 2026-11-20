from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='core/login.html'),
        name='login'
    ),
    path(
        'logout/',
        views.simple_logout,   # uses the custom logout view in core/views.py
        name='logout'
    ),

    # App views
    path('', views.home, name='home'),
    path('payroll-summary/', views.payroll_summary, name='payroll_summary'),
    path('log-time/', views.log_time, name='log_time'),
    path('time-entries/', views.time_entries_list, name='time_entries_list'),
    path('clients/', views.clients_list, name='clients_list'),
    path('clients/new/', views.create_client, name='create_client'),
    path('invoices/', views.invoices_list, name='invoices_list'),
    path('invoices/new/', views.create_invoice, name='create_invoice'),
    path('invoices/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
]
