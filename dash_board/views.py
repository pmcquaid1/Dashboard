from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Shipment, Packlist, Employee
from .forms import PacklistForm, EmployeeForm, PretripForm
from django.contrib import messages
from .models import FuelReq, Pretrip

# ✅ Added for login functionality
from django.contrib.auth import authenticate, login, logout

# View for displaying a base template
def base(request):
    return render(request, 'base.html')

# View for displaying a landing page
def landing(request):
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    user = request.user
    sections = []
    cards = []

    if user.groups.filter(name='Operations').exists():
        sections.append({"name": "Operations", "url": "ops", "color": "primary"})
        cards.append({
            "title": "Operations",
            "description": "Access delivery schedules, route planning tools, and fleet management reports.",
            "class": "card-ops",
            "url": "ops",
            "link_text": "Ops Staff Access Here"
        })

    if user.groups.filter(name='Finance').exists():
        sections.append({"name": "Finance", "url": "finance", "color": "warning"})
        cards.append({
            "title": "Finance",
            "description": "Budget reports, expense tracking, and invoice management tools for finance staff.",
            "class": "card-finance",
            "url": "finance",
            "link_text": "Finance Staff Access Here"
        })

    if user.groups.filter(name='QHSE').exists():
        sections.append({"name": "QHSE", "url": "qhse", "color": "success"})
        cards.append({
            "title": "QHSE",
            "description": "Safety protocols, audit logs, and compliance documentation for QHSE staff.",
            "class": "card-qhse",
            "url": "qhse",
            "link_text": "QHSE Staff Access Here"
        })

    if user.groups.filter(name='HR').exists():
        sections.append({"name": "Human Resources", "url": "hr_support", "color": "danger"})
        cards.append({
            "title": "Human Resources",
            "description": "Employee records, training modules, and HR policies accessible to all staff.",
            "class": "card-hr",
            "url": "hr_support",
            "link_text": "All Staff Access Here"
        })

    return render(request, 'dashboard.html', {
        'sections': sections,
        'cards': cards,
        'user': user
    })

@permission_required('app.view_operations', raise_exception=True)
@login_required
def ops(request):
    month_labels, month_counts = get_monthly_shipment_counts()
    context = {
        'month_labels': month_labels,
        'month_counts': month_counts,
    }
    return render(request, 'ops.html', context)

@permission_required('app.view_finance', raise_exception=True)
@login_required
def finance(request):
    month_labels, month_counts = get_monthly_shipment_counts()
    context = {
        'month_labels': month_labels,
        'month_counts': month_counts,
    }
    return render(request, 'finance.html', context)

@permission_required('app.view_qhse', raise_exception=True)
@login_required
def qhse(request):
    month_labels, month_counts = get_monthly_shipment_counts()
    context = {
        'month_labels': month_labels,
        'month_counts': month_counts,
    }
    return render(request, 'qhse.html', context)

@permission_required('app.view_hr', raise_exception=True)
@login_required
def hr_support(request):
    month_labels, month_counts = get_monthly_shipment_counts()
    context = {
        'month_labels': month_labels,
        'month_counts': month_counts,
    }
    return render(request, 'hr_support.html', context)

def shipments(request):
    return render(request, 'shipments.html')

def add_shipment(request):
    return render(request, 'add_shipment.html')

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

@login_required
def register(request):
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

def signature(request, pk, model_type):
    model_map = {
        'fuelreq': FuelReq,
        'pretrip': Pretrip,
    }
    model = model_map.get(model_type)
    if not model:
        return HttpResponse("Invalid model type", status=400)

    record = get_object_or_404(model, pk=pk)
    return render(request, 'signature.html', {'record': record})

@login_required
def pretrip(request):
    if request.method == 'POST':
        form = PretripForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pretrip record submitted successfully.")
            return redirect('pretrip')
    else:
        form = PretripForm()

    pretrips = Pretrip.objects.all().order_by('-date')
    return render(request, 'pretrip_form.html', {'form': form, 'pretrips': pretrips})

def clearing_table(request):
    return render(request, 'clearing_table.html')

def transport_table(request):
    return render(request, 'transport_table.html')

def charts(request):
    return render(request, 'charts.html')

def get_monthly_shipment_counts():
    results = Shipment.objects.annotate(
        month=TruncMonth("actual_delivery")
    ).values("month").annotate(
        count=Count("shipment_id")
    ).order_by("month")

    month_labels = [r["month"].strftime("%B") for r in results]
    month_counts = [r["count"] for r in results]
    return month_labels, month_counts

def edit(request):
    return render(request, 'edit.html')

def delete(request):
    return render(request, 'delete.html')

def upload(request):
    return render(request, 'upload.html')

def forms(request):
    return render(request, 'forms.html')

def forms2(request):
    return render(request, 'forms2.html')

def invoice(request):
    return render(request, 'invoice.html')

def lineitems(request):
    return render(request, 'lineitems.html')

def create_packlist(request):
    return render(request, 'create_packlist.html')

def purchase_order(request):
    return render(request, 'purchase_order.html')

def add_bl2(request):
    return render(request, 'add_bl2.html')

def bills(request):
    return render(request, 'bills.html')

def add_bill(request):
    return render(request, 'add_bill.html')

def waybill(request):
    return render(request, 'waybill.html')

def organization(request):
    return render(request, 'organization.html')

def vieworganization(request):
    return render(request, 'vieworganization.html')

def detail_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'detail_view.html', {'employee': employee})

def transport_job_detail(request):
    return render(request, 'transport_job_detail.html')

def fuelreq(request):
    return render(request, 'fuelreq.html')

# ✅ Fixed login_user view
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')



# ✅ Fixed logout_user view
def logout_user(request):
    logout(request)
    return redirect('landing')

def update_user(request):
    if request.method == 'POST':
        pass
    return render(request, 'update_user.html')

def update_password(request):
    if request.method == 'POST':
        pass
    return render(request, 'update_password.html')

def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def my_view(request):
    return render(request, 'my_view.html')


# This file contains views for the Dash Board application.
# Each view corresponds to a specific functionality or page in the application.
# The views are decorated with login_required and permission_required to ensure that only authorized users can access them.



# Additional views can be added here following the same pattern
