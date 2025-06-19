
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Shipment, Packlist, Employee
from .forms import PacklistForm, EmployeeForm, PretripForm # ✅ Make sure PretripForm is imported
from django.contrib import messages
from .models import FuelReq, Pretrip  #whatever model stores the signature

# View for displaying a base template
def base(request):
    return render(request, 'base.html')

# View for displaying a landing page
def landing(request):
    return render(request, 'landing.html')

# Dashboard view
@login_required
def dashboard(request):
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

    return render(request, 'dashboard.html', {'sections': sections})

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

# Shipments View
def shipments(request):
    return render(request, 'shipments.html')

# Add Shipment View
def add_shipment(request):
    return render(request, 'add_shipment.html')

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

# View for displaying a saved signature
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

# View for submitting and listing Pretrip records
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

# View Clearing Table 
def clearing_table(request):
    return render(request, 'clearing_table.html')

# View Transport Table 
def transport_table(request):
    return render(request, 'transport_table.html')

# View Charts 
def charts(request):
    return render(request, 'charts.html')

# Utility functions

# For aggregating shipments by month
def get_monthly_shipment_counts():
    results = Shipment.objects.annotate(
        month=TruncMonth("actual_delivery")
    ).values("month").annotate(
        count=Count("shipment_id")
    ).order_by("month")

    month_labels = [r["month"].strftime("%B") for r in results]
    month_counts = [r["count"] for r in results]
    return month_labels, month_counts

# For Editing 
def edit(request):
    return render(request, 'edit.html')

# For Deleting
def delete(request):
    return render(request, 'delete.html')

# For Upload
def upload(request):
    return render(request, 'upload.html')

# For Forms
def forms(request):
    return render(request, 'forms.html')

# For Invoice
def invoice(request):
    return render(request, 'invoice.html')

# For lineitems
def lineitems(request):
    return render(request, 'lineitems.html')

# For create_packlist
def create_packlist(request):
    return render(request, 'create_packlist.html')
# For purchase_order
def purchase_order(request):
    return render(request, 'purchase_order.html')

# For add_bl2   
def add_bl2(request):
    return render(request, 'add_bl2.html')  

# For bills 
def bills(request):
    return render(request, 'bills.html')    

# For add_bill  
def add_bill(request):
    return render(request, 'add_bill.html') 

# For waybill   
def waybill(request):
    return render(request, 'waybill.html')

# For organization  
def organization(request):
    return render(request, 'organization.html')

# For vieworganization
def vieworganization(request):
    return render(request, 'vieworganization.html')

# For detail_view   
def detail_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'detail_view.html', {'employee': employee})

# For transport_job_detail
def transport_job_detail(request):
    return render(request, 'transport_job_detail.html') 

# For fuelreq
def fuelreq(request):
    return render(request, 'fuelreq.html')

# For login_user
def login_user(request):
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, 'login.html')

# For logout_user
def logout_user(request):
    # Handle logout logic here
    return redirect('landing')  

# For update_user
def update_user(request):
    if request.method == 'POST':
        # Handle user update logic here
        pass
    return render(request, 'update_user.html')

# For update_password
def update_password(request):
    if request.method == 'POST':
        # Handle password update logic here
        pass
    return render(request, 'update_password.html')

# For profile
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

# For my_view
def my_view(request):
    # This is a placeholder for any custom view logic
    return render(request, 'my_view.html')

# This file contains views for the Dash Board application.
# Each view corresponds to a specific functionality or page in the application.
# The views are decorated with login_required and permission_required to ensure that only authorized users can access them.



# Additional views can be added here following the same pattern
