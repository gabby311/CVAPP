from datetime import date

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Employee, TimeEntry, Invoice, InvoiceLine, Client
from .forms import TimeEntryForm, InvoiceForm, ClientForm


def simple_logout(request):
    """
    Simple logout view: logs out the user and redirects to login page.
    """
    logout(request)
    return redirect('login')


@login_required
def home(request):
    return render(request, 'core/home.html')


@login_required
def payroll_summary(request):
    """
    Show total hours and gross pay per employee for a given date range.
    """
    today = date.today()
    default_start = date(today.year, today.month, 1)
    default_end = today

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
    else:
        start_date = default_start
        end_date = default_end

    time_entries = TimeEntry.objects.filter(date__gte=start_date, date__lte=end_date)

    hours_by_employee = (
        time_entries
        .values('employee')
        .annotate(total_hours=Sum('hours_worked'))
    )

    payroll_rows = []
    for row in hours_by_employee:
        employee = Employee.objects.get(id=row['employee'])
        total_hours = row['total_hours'] or 0
        gross_pay = 0

        if employee.pay_type == 'hourly' and employee.hourly_rate:
            gross_pay = total_hours * employee.hourly_rate
        elif employee.pay_type == 'salary' and employee.monthly_salary:
            # Simple assumption: full monthly salary for the period
            gross_pay = employee.monthly_salary

        payroll_rows.append({
            'employee': employee,
            'total_hours': total_hours,
            'gross_pay': gross_pay,
        })

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'payroll_rows': payroll_rows,
    }
    return render(request, 'core/payroll_summary.html', context)


@login_required
def log_time(request):
    """
    Form to create a new TimeEntry.
    """
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('time_entries_list')
    else:
        form = TimeEntryForm()

    return render(request, 'core/log_time.html', {'form': form})


@login_required
def time_entries_list(request):
    """
    List all time entries, newest first.
    """
    entries = (
        TimeEntry.objects
        .select_related('employee', 'client')
        .order_by('-date')
    )
    return render(request, 'core/time_entries_list.html', {'entries': entries})


@login_required
def clients_list(request):
    """
    List all clients.
    """
    clients = Client.objects.all().order_by('name')
    return render(request, 'core/clients_list.html', {'clients': clients})


@login_required
def create_client(request):
    """
    Create a new client.
    """
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm()

    return render(request, 'core/create_client.html', {'form': form})


@login_required
def invoices_list(request):
    """
    List all invoices.
    """
    invoices = (
        Invoice.objects
        .select_related('client')
        .order_by('-issue_date')
    )
    return render(request, 'core/invoices_list.html', {'invoices': invoices})


@login_required
def create_invoice(request):
    """
    Create a new invoice (basic manual form).
    """
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            if invoice.total_amount is None:
                invoice.total_amount = 0
            invoice.save()
            return redirect('invoices_list')
    else:
        form = InvoiceForm()

    return render(request, 'core/create_invoice.html', {'form': form})


@login_required
def invoice_detail(request, invoice_id):
    """
    Show a single invoice with its line items in a printable layout.
    """
    invoice = get_object_or_404(Invoice, id=invoice_id)
    lines = InvoiceLine.objects.filter(invoice=invoice)
    return render(request, 'core/invoice_detail.html', {
        'invoice': invoice,
        'lines': lines,
    })
