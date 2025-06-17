
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Shipment, Packlist, Employee
from .forms import PacklistForm, EmployeeForm
from django.contrib import messages

# Utility function for aggregating shipments by month
def get_monthly_shipment_counts():
    results = Shipment.objects.annotate(
        month=TruncMonth("actual_delivery")
    ).values("month").annotate(
        count=Count("shipment_id")
    ).order_by("month")

    month_labels = [r["month"].strftime("%B") for r in results]
    month_counts = [r["count"] for r in results]
    return month_labels, month_counts

# Dashboard view
@login_required
def home(request):
    user = request.user
    sections = []

    if user.groups.filter(name='Operations').exists():
        sections.append({"name": "Operations", "url": "ops", "color": "primary"})

    if user.groups.filter(name='Finance').exists():
        sections.append({"name": "Finance", "url": "finance", "color": "warning"})

    if user.groups.filter(name='QHSE').exists():
        sections.append({"name": "QHSE", "url": "qhse", "color": "success"})

    if user.groups.filter(name='HR').exists():
        sections.append({"name": "HR Resources", "url": "hr_support", "color": "danger"})

    return render(request, 'home.html', {'sections': sections})

# Operations view
@login_required
@permission_required('app.view_operations', raise_exception=True)
def ops(request):
    month_labels, month_counts = get_monthly_shipment_counts()
    context = {
        'month_labels': month_labels,
        'month_counts': month_counts,
    }
    return render(request, 'ops.html', context)

# Finance view
@login_required
@permission_required('app.view_finance', raise_exception=True)
def finance(request):
    month_labels, month_counts = get_monthly_shipment_counts()
    context = {
        'month_labels': month_labels,
        'month_counts': month_counts,
    }
    return render(request, 'finance.html', context)

# QHSE view
@login_required
@permission_required('app.view_qhse', raise_exception=True)
def qhse(request):
    month_labels, month_counts = get_monthly_shipment_counts()
    context = {
        'month_labels': month_labels,
        'month_counts': month_counts,
    }
    return render(request, 'qhse.html', context)

# HR Resources view
@login_required
@permission_required('app.view_hr', raise_exception=True)
def hr_support(request):
    month_labels, month_counts = get_monthly_shipment_counts()
    context = {
        'month_labels': month_labels,
        'month_counts': month_counts,
    }
    return render(request, 'hr_support.html', context)


# Packlist view
@login_required
def packlist(request):
    if request.method == 'POST':
        form = PacklistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('packlist')
    else:
        form = PacklistForm()
    context = {'form': form, 'packlists': Packlist.objects.all()}
    return render(request, 'packlist.html', context)

# Employee view
@login_required
def register_user(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = form.save()
            department = form.cleaned_data.get('department')
            position = form.cleaned_data.get('position')
            Employee.objects.create(user=user, department=department, position=position)
            messages.success(request, "Employee registered successfully.")
            return redirect('employee_confirmation')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})



# Additional views can be added here following the same pattern
