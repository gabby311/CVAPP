from django import forms

from .models import TimeEntry, Invoice, InvoiceLine, Client


class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = TimeEntry
        fields = ['employee', 'client', 'date', 'hours_worked', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'invoice_number', 'issue_date', 'due_date', 'status', 'notes']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'contact_name', 'email', 'billing_address', 'payment_terms_days']
