from django.contrib import admin

from .models import Employee, Client, TimeEntry, Invoice, InvoiceLine


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'pay_type', 'hourly_rate', 'monthly_salary', 'is_active')
    list_filter = ('pay_type', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'email', 'payment_terms_days')
    search_fields = ('name', 'contact_name', 'email')


@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'employee', 'client', 'hours_worked')
    list_filter = ('date', 'employee', 'client')
    search_fields = ('employee__first_name', 'employee__last_name', 'client__name')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client', 'issue_date', 'due_date', 'status', 'total_amount')
    list_filter = ('status', 'issue_date', 'client')
    search_fields = ('invoice_number', 'client__name')


@admin.register(InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'quantity', 'unit_price', 'line_total')
    search_fields = ('invoice__invoice_number', 'description')
