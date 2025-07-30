from uuid import uuid4
import csv
from io import StringIO
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Shipment, Packlist, Employee, FuelReq, Pretrip
from .forms import PacklistForm, EmployeeForm, FuelReqForm, PretripForm
import re
from decimal import Decimal


def clean_phone_number(raw):
    if not raw:
        return ""
    raw = raw.strip()

    # ✅ Safer conversion using Decimal to avoid losing digits
    try:
        if re.match(r"^\d+(\.\d+)?[eE][+-]?\d+$", raw):
            raw = str(Decimal(raw))
    except Exception:
        pass

    return raw

def base(request):
    return render(request, 'base.html')

@csrf_exempt
def import_employees(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        file = request.FILES["csv_file"]
        data = file.read().decode("utf-8-sig")
        reader = csv.DictReader(StringIO(data))

        created_count = 0
        for row in reader:
            if not any(row.values()):
                continue  # Skip empty rows

            email = row.get("email", "").strip()
            if not email:
                email = f"placeholder_{uuid4().hex[:8]}@example.com"

            try:
                base_username = email.split("@")[0]
                unique_username = f"{base_username}_{uuid4().hex[:4]}"
                user, _ = User.objects.get_or_create(email=email, defaults={"username": unique_username})

                # ✅ Check if this user already has an employee record
                if not Employee.objects.filter(user=user).exists():
                    Employee.objects.create(
                        user=user,
                        first_name=row.get("first_name", "").strip(),
                        last_name=row.get("last_name", "").strip(),
                        department=row.get("department", "").strip(),
                        position=row.get("position", "").strip(),
                        location=row.get("location", "").strip(),
                        company=row.get("company", "").strip(),
                        phone=clean_phone_number(row.get("phone", "")),
                        email=email  # ✅ Add this line
                    )
                    created_count += 1
                else:
                    print(f"Skipped duplicate employee for user: {user.username}")

            except Exception as e:
                print(f"Failed to import row: {row}\nError: {e}")

        return JsonResponse({
            "status": "Import completed",
            "file": file.name,
            "created": created_count
        })

    return JsonResponse({"error": "No file uploaded"}, status=400)




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
            "class": "card-ops", "url": "ops", "link_text": "Ops Staff Access Here"
        })

    if user.groups.filter(name='Finance').exists():
        sections.append({"name": "Finance", "url": "finance", "color": "warning"})
        cards.append({
            "title": "Finance",
            "description": "Budget reports, expense tracking, and invoice management tools for finance staff.",
            "class": "card-finance", "url": "finance", "link_text": "Finance Staff Access Here"
        })

    if user.groups.filter(name='QHSE').exists():
        sections.append({"name": "QHSE", "url": "qhse", "color": "success"})
        cards.append({
            "title": "QHSE",
            "description": "Safety protocols, audit logs, and compliance documentation for QHSE staff.",
            "class": "card-qhse", "url": "qhse", "link_text": "QHSE Staff Access Here"
        })

    if user.groups.filter(name='HR').exists():
        sections.append({"name": "Human Resources", "url": "hr_support", "color": "danger"})
        cards.append({
            "title": "Human Resources",
            "description": "Employee records, training modules, and HR policies accessible to all staff.",
            "class": "card-hr", "url": "hr_support", "link_text": "All Staff Access Here"
        })

    return render(request, 'dashboard.html', {'sections': sections, 'cards': cards, 'user': user})

@login_required
def ops(request): return render(request, 'ops.html')

@login_required
def finance(request): return render(request, 'finance.html')

@login_required
def qhse(request): return render(request, 'qhse.html')

@login_required
def hr_support(request): return render(request, 'hr_support.html')

def shipments(request): return render(request, 'shipments.html')

def add_shipment(request): return render(request, 'add_shipment.html')

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
def import_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        file = request.FILES["csv_file"]
        data = file.read().decode("utf-8-sig")
        reader = csv.DictReader(StringIO(data))

        created_count = 0
        for row in reader:
            if not any(row.values()):
                continue

            email = row.get("email", "").strip()
            if not email:
                email = f"placeholder_{uuid4().hex[:8]}@example.com"

            try:
                username = email.split("@")[0]
                user, _ = User.objects.get_or_create(username=username, email=email)
                print(f"Creating employee with email: {email}")

                Employee.objects.create(
                    user=user,
                    first_name=row.get("first_name", "").strip(),
                    last_name=row.get("last_name", "").strip(),
                    department=row.get("department", "").strip(),
                    position=row.get("position", "").strip(),
                    location=row.get("location", "").strip(),
                    company=row.get("company", "").strip(),
                    phone = clean_phone_number(row.get("phone", "")),
                    email=email  # ✅ Add this line

                )
                created_count += 1
            except Exception as e:
                print(f"Failed to import row: {row}\nError: {e}")

        messages.success(request, f"Successfully imported {created_count} employees from '{file.name}'.")
    return render(request, "employee_form.html", {"form": EmployeeForm()})

@login_required
def register(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            user = form.save()
            Employee.objects.create(
                user=user,
                department=form.cleaned_data.get('department'),
                position=form.cleaned_data.get('position')
            )
            messages.success(request, "Employee registered successfully.")
            return redirect('employee_confirmation')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

def signature(request, pk, model_type):
    model_map = {'fuelreq': FuelReq, 'pretrip': Pretrip}
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

# Static views
def clearing_table(request): return render(request, 'clearing_table.html')
def transport_table(request): return render(request, 'transport_table.html')
def charts(request): return render(request, 'charts.html')
def edit(request): return render(request, 'edit.html')
def delete(request): return render(request, 'delete.html')
def upload(request): return render(request, 'upload.html')
def forms(request): return render(request, 'forms.html')
def forms2(request): return render(request, 'forms2.html')
def invoice(request): return render(request, 'invoice.html')
def lineitems(request): return render(request, 'lineitems.html')
def create_packlist(request): return render(request, 'create_packlist.html')
def purchase_order(request): return render(request, 'purchase_order.html')
def add_bl2(request): return render(request, 'add_bl2.html')
def bills(request): return render(request, 'bills.html')
def add_bill(request): return render(request, 'add_bill.html')
def waybill(request): return render(request, 'waybill.html')
def organization(request): return render(request, 'organization.html')
def vieworganization(request): return render(request, 'vieworganization.html')

def detail_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'detail_view.html', {'employee': employee})

def transport_job_detail(request): return render(request, 'transport_job_detail.html')

@login_required
def fuelreq(request):
    if request.method == 'POST':
        form = FuelReqForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fuel request submitted successfully.")
            return redirect('fuelreq')
    else:
        form = FuelReqForm()
    return render(request, 'fuelreq.html', {'form': form})

@login_required
def signature(request, pk):
    req = get_object_or_404(FuelReq, pk=pk)
    if request.method == 'POST':
        req.signed_by_driver = True
        req.driver_verified_at = now()
        req.signature_data_url = request.POST.get('signature')
        req.save()
        messages.success(request, "Fuel request signed successfully.")
        return redirect('dashboard')
    return render(request, 'fuelreq_sign.html', {'request_obj': req})

def fuelreq_sign(request, pk):
    fuelreq = get_object_or_404(FuelReq, pk=pk)
    if request.method == 'POST':
        fuelreq.signed_by_driver = True
        fuelreq.driver_verified_at = now()
        fuelreq.signature_data_url = request.POST.get('signature')
        fuelreq.save()
        messages.success(request, "Fuel request signed successfully.")
        return redirect('signature_confirmation')
    return render(request, 'fuelreq_sign.html', {'fuelreq': fuelreq})

@login_required
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # or your preferred landing view
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return render(request, 'logout.html', {
        'message': 'You have been successfully logged out.'
    })

@login_required
def update_user(request):
    if request.method == 'POST':
        pass
    return render(request, 'update_user.html')

@login_required
def update_password(request):
    if request.method == 'POST':
        pass
    return render(request, 'update_password.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def my_view(request):
    return render(request, 'my_view.html')