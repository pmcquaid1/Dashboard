# 🔝 Imports
import csv
import logging
import re
from decimal import Decimal
from io import StringIO
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt

from import_export.formats.base_formats import CSV
from tablib import Dataset

from .forms import PacklistForm, EmployeeForm, FuelReqForm, PretripForm
from .models import Shipment, Packlist, Employee, FuelReq, Pretrip
from .resources import EmployeeResource

from django.urls import get_resolver


def list_routes(request):
    urls = [str(p.pattern) for p in get_resolver().url_patterns]
    return JsonResponse({"routes": urls})

print("✅ views.py loaded")

logger = logging.getLogger(__name__)

def test_home(request):
    logger.info("Test home accessed from %s", request.META.get("REMOTE_ADDR"))

    banner = ""
    if getattr(settings, "DRY_RUN_MODE", False):
        banner = "<div style='background:#ffc;padding:10px;text-align:center;'>⚠️ Test Environment – Data may be reset</div>"

    return HttpResponse(f"""
        {banner}
        <h1>Welcome to SLLHub Test Environment</h1>
        <p>This is a safe space for dry-run testing and vendor validation.</p>
    """)

# 🔐 Rate limiting config
RATE_LIMIT_KEY = "login_attempts:{ip}"
RATE_LIMIT_MAX = 5
RATE_LIMIT_WINDOW = 300  # seconds

logger = logging.getLogger(__name__)

# 🔧 Utility functions
def get_client_ip(request):
    return request.META.get('REMOTE_ADDR', 'unknown')

def clean_phone_number(raw):
    if not raw:
        return ""
    raw = raw.strip()
    try:
        if re.match(r"^\d+(\.\d+)?[eE][+-]?\d+$", raw):
            raw = str(Decimal(raw))
    except Exception:
        pass
    return raw

# 🔧 Department card configuration
DEPARTMENT_CARD_CONFIG = {
    "Transport": {
        "description": "Access delivery schedules, route planning tools, and fleet management reports.",
        "class": "card-transport",
        "url": "transport",
        "link_text": "Transport Staff Access Here",
        "color": "primary",
    },
    "Finance": {
        "description": "Budget reports, expense tracking, and invoice management tools for finance staff.",
        "class": "card-finance",
        "url": "finance",
        "link_text": "Finance Staff Access Here",
        "color": "warning",
    },
    "QHSE": {
        "description": "Safety protocols, audit logs, and compliance documentation for QHSE staff.",
        "class": "card-qhse",
        "url": "qhse",
        "link_text": "QHSE Staff Access Here",
        "color": "success",
    },
    "HR": {
        "description": "Employee records, training modules, and HR policies accessible to all staff.",
        "class": "card-hr",
        "url": "hr_support",
        "link_text": "All Staff Access Here",
        "color": "danger",
    },
    "Warehouse": {
        "description": "Warehouse records, Forms, etc.",
        "class": "card-warehouse",
        "url": "warehouse",
        "link_text": "Warehouse Staff Access Here",
        "color": "danger",
    },
    "RevOps": {
        "description": "RevOps records, Forms, etc.",
        "class": "card-revops",
        "url": "revops",
        "link_text": "Revops Staff Access Here",
        "color": "danger",
    },
    "C&F": {
        "description": "Clearing records, Forms, etc.",
        "class": "card-cf",
        "url": "c_f",
        "link_text": "C&F Staff Access Here",
        "color": "danger",
    },
    "Documentation": {
        "description": "ICUMS, BOE, Forms, etc.",
        "class": "card-docs",
        "url": "documentation",
        "link_text": "Documentation Staff Access Here",
        "color": "danger",
    },
}
@csrf_exempt
def import_employees(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        file = request.FILES["csv_file"]
        data = file.read().decode("utf-8-sig")
        reader = csv.DictReader(StringIO(data))

        created_count = 0
        updated_count = 0

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

                # 🔹 Sync first and last name to User model
                user.first_name = row.get("first_name", "").strip()
                user.last_name = row.get("last_name", "").strip()
                user.save()

                # 🔹 Log user creation/update
                print(f"{'Created' if _ else 'Updated'} user: {email} ({user.first_name} {user.last_name})")

                employee = Employee.objects.filter(user=user).first()
                if employee:
                    # Update existing employee record
                    employee.first_name = row.get("first_name", "").strip()
                    employee.last_name = row.get("last_name", "").strip()
                    employee.department = row.get("department", "").strip()
                    employee.position = row.get("position", "").strip()
                    employee.location = row.get("location", "").strip()
                    employee.company = row.get("company", "").strip()
                    employee.phone = clean_phone_number(row.get("phone", ""))
                    employee.email = email
                    employee.save()
                    updated_count += 1
                    print(f"🔄 Updated employee: {email} (Dept: {employee.department})")
                else:
                    # Create new employee record
                    Employee.objects.create(
                        user=user,
                        first_name=row.get("first_name", "").strip(),
                        last_name=row.get("last_name", "").strip(),
                        department=row.get("department", "").strip(),
                        position=row.get("position", "").strip(),
                        location=row.get("location", "").strip(),
                        company=row.get("company", "").strip(),
                        phone=clean_phone_number(row.get("phone", "")),
                        email=email
                    )
                    created_count += 1
                    print(f"✅ Created employee: {email}")

            except Exception as e:
                print(f"❌ Failed to import row: {row}\nError: {e}")

        return JsonResponse({
            "status": "Import completed",
            "file": file.name,
            "created": created_count,
            "updated": updated_count
        })

    return JsonResponse({"error": "No file uploaded"}, status=400)
# 🔐 Login view (corrected)
@csrf_exempt
def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')
        ip = get_client_ip(request)
        key = RATE_LIMIT_KEY.format(ip=ip)
        attempts = cache.get(key) or 0

        if attempts >= RATE_LIMIT_MAX:
            messages.error(request, 'Too many login attempts. Please wait a few minutes.')
            logger.warning(f"[RATE LIMIT] IP={ip} blocked after {attempts} attempts")
            return render(request, 'login.html')

        user = None
        reason = ""
        user_obj = None

        try:
            matches = User.objects.filter(email__iexact=identifier) if '@' in identifier else User.objects.filter(username=identifier)

            if matches.count() > 1:
                logger.warning(f"⚠️ Duplicate identifier detected: {identifier} ({matches.count()} users)")

            user_obj = matches.first()

            if user_obj:
                logger.debug(f"[AUTH DEBUG] identifier={identifier}, resolved_username={user_obj.username}, resolved_email={user_obj.email}")

                if not user_obj.is_active:
                    reason = "User is inactive"
                else:
                    user = authenticate(request, username=user_obj.username, password=password)
                    if user is None:
                        reason = "Incorrect password"
            else:
                reason = "User not found"

        except Exception as e:
            reason = f"Unexpected error during login: {str(e)}"
            logger.exception(f"[LOGIN ERROR] identifier={identifier}, ip={ip}, error={str(e)}")

        if user:
            login(request, user)
            logger.info(f"[LOGIN SUCCESS] user={user.username}, ip={ip}, time={now()}")
            cache.delete(key)
            return redirect('dashboard')
        else:
            cache.set(key, attempts + 1, RATE_LIMIT_WINDOW)
            messages.error(request, f"Login failed: {reason}")
            logger.warning(f"[LOGIN FAIL] identifier={identifier}, ip={ip}, reason={reason}, time={now()}")

    return render(request, 'login.html')


# 🔐 Logout view
def logout_user(request):
    logout(request)
    return render(request, 'logout.html', {'message': 'You have been successfully logged out.'})

# 🧭 Landing and dashboard
def landing(request):
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    user = request.user
    user_groups = set(user.groups.values_list('name', flat=True))
    cards = []
    sections = []

    visible_departments = DEPARTMENT_CARD_CONFIG.keys() if user.is_superuser else user_groups

    for dept in visible_departments:
        config = DEPARTMENT_CARD_CONFIG.get(dept)
        if config:
            sections.append({
                "name": dept,
                "url": config["url"],
                "color": config["color"],
            })
            cards.append({
                "title": dept,
                "description": config["description"],
                "class": config["class"],
                "url": config["url"],
                "link_text": config["link_text"],
            })
        else:
            cards.append({
                "title": dept,
                "description": f"Resources for {dept} department.",
                "class": "card-generic",
                "url": dept.lower(),
                "link_text": f"{dept} Access",
            })

    return render(request, 'dashboard.html', {
        'sections': sections,
        'cards': cards,
        'user': user,
    })
# 📦 Department views
@login_required
def transport(request):
    return render(request, 'transport.html')

@login_required
def finance(request):
    return render(request, 'finance.html')

@login_required
def qhse(request):
    return render(request, 'qhse.html')

@login_required
def hr_support(request):
    return render(request, 'hr_support.html')

@login_required
def warehouse(request):
    return render(request, 'warehouse.html')

@login_required
def revops(request):
    return render(request, 'revops.html')

@login_required
def c_f(request):
    return render(request, 'c_f.html')

@login_required
def documentation(request):
    return render(request, 'documentation.html')

# 📄 Static views
def base(request):
    return render(request, 'base.html')

def shipment_test(request):
    return render(request, 'shipment_test.html')

from django.http import HttpResponse

def document_test(request):
    logger.warning("📍 document_test view executed")
    return HttpResponse("✅ document_test view executed")





def add_shipment(request):
    return render(request, 'add_shipment.html')

def clearing_table(request):
    return render(request, 'clearing_table.html')

def transport_table(request):
    return render(request, 'transport_table.html')

def charts(request):
    return render(request, 'charts.html')

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

def my_view(request):
    return render(request, 'my_view.html')

# 👤 Profile and update views
@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def update_user(request):
    return render(request, 'update_user.html')

@login_required
def update_password(request):
    return render(request, 'update_password.html')

# 📋 Packlist view
@login_required
def packlist(request):
    if request.method == 'POST':
        form = PacklistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('packlist')
    else:
        form = PacklistForm()
    return render(request, 'packlist.html', {
        'form': form,
        'packlists': Packlist.objects.all()
    })

# 📥 CSV import via tablib
@login_required
def import_csv(request):
    if request.method == "POST" and request.FILES.get("csv_file"):
        file = request.FILES["csv_file"]
        data = file.read().decode("utf-8-sig")
        dataset = Dataset().load(data, format="csv")
        resource = EmployeeResource()
        result = resource.import_data(dataset, dry_run=False, raise_errors=False)
        messages.success(request, f"Successfully imported {resource.row_success} employees from '{file.name}'.")
    return render(request, "employee_form.html", {"form": EmployeeForm()})

# 🧾 Employee registration
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

# 🖋️ Signature views
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

def signature_generic(request, pk, model_type):
    model_map = {
        'fuelreq': FuelReq,
        'pretrip': Pretrip
    }
    model = model_map.get(model_type)
    if not model:
        return HttpResponse("Invalid model type", status=400)
    record = get_object_or_404(model, pk=pk)
    return render(request, 'signature.html', {'record': record})

# ⛽ Fuel request form
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

# 🚐 Pretrip form
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
    return render(request, 'pretrip_form.html', {
        'form': form,
        'pretrips': pretrips
    })

# 🔍 Detail view
def detail_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    return render(request, 'detail_view.html', {'employee': employee})

# 🚚 Transport job detail
def transport_job_detail(request):
    return render(request, 'transport_job_detail.html')

def ping(request):
    return HttpResponse("✅ Django is running and routing is working.")