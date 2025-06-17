
def aggregate_shipments_by_month(shipments):
    aggregated_data = shipments.annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('quantity')).order_by('month')
    return aggregated_data

from calendar import HTMLCalendar
import calendar
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Shipment
from .models import Transport
from .models import Bill
from .models import Organization
from .models import FuelReq
from .forms import ShipmentForm
from .forms import BillForm
from .forms import InvoiceForm
from .forms import PacklistForm
from .forms import FuelReqForm
from .forms import BillForm2
from .forms import WaybillForm
from .models import Packlist
from django.contrib import messages
from .forms import UpdateContact, SignUpForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.views.generic import TemplateView
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum


@login_required
def profile(request):
    return render(request, 'profile.html')


def my_view(request):
    all_transports = Transport.objects.all()()
    context = {
        'all_transports': all_transports,
    }
    return render(request, 'transport_table.html', context)

def detail_view(request, id):
    record = get_object_or_404(Transport, id=id)
    context = {
        'record': record,
    }
    return render(request, 'transport_job_detail.html', context)

def transport_job_detail(request):
	return render(request, 'transport_job_detail.html', {})

class ShipmentChartView(TemplateView):
	template_name='charts2.html'
	def get_context_data(self, **kwargs):
		context=super(ShipmentChartView, self).get_context_data(**kwargs)
		context["qs"]= Shipment.objects.all()()
		return context

def base(request):
	return render(request, 'base.html', {})

def charts2(request):
		# Step 1 Aggregating shipments within the month
	results = Shipment.objects.annotate(
		month=TruncMonth("actual_delivery"),
	).values(
		"month"
	).annotate(
		count=Count("shipment_id"),
		#total_weight=Sum("weight")

	).order_by("month")
	print(results)

	# Step 2 Take the results and parse to the format to be fed to the html page(charts2)
	"""<QuerySet [{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 11, 1), 'count': 1}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 10, 1), 'count': 70}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 9, 1), 'count': 5}]>
  	"""
	month_labels = []
	month_counts = []

	for record in results:
		month_counts.append(record["count"])
		month_labels.append(record["month"].strftime("%B"))

	return render(request, 'charts2.html', {
		"months": month_labels,
		"data": month_counts,
	})

def login_user(request):
	if request.method=="POST":
		#grab form info
		username= request.POST['username']
		password= request.POST['password']
		user= authenticate(request, username=username, password=password)
		
		if user is not None:
			login(request,user)
			messages.success(request, "User Login Successful")
			return redirect('home2')
		
		else:
			messages.success(request, "Login Unsuccessful")
			return redirect('login')
	else:
		return render(request,'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, "User Logout Successful")
	return redirect('home1')

def register_user(request):
	form = SignUpForm()
	if request.method =="POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			#log use in
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# Authenticate
			user = authenticate(username=username, password=password)
			# log in
			login(request, user)
			messages.success(request, "User Login Successful")
			return redirect('home2')
		
		else:
			messages.success(request, "Login Unsuccessful")
			return redirect('register')

	else:
		return render(request, 'register.html', {'form':form})	

def update_user(request):
	if request.user.is_authenticated:
		#get current user
		current_user=User.objects.get(id=request.user.id)
		#create our form
		user_form=UpdateUserForm(request.POST or None, instance=current_user)
		#update and save user info
		if user_form.is_valid():
			user_form.save()
		# Log user back in
			login(request, current_user)
			messages.success(request, ("Your User Info Has Been Updated"))
			return redirect('home1')	
		return render(request, 'update_user.html', {'user_form':user_form})

	else:
		messages.success(request, "Must Be Logged In To Update Your User Info")
		return redirect('login')

def update_password(request):
	return render(request, 'update_password.html', {})

def home1(request):
    sections = ["Operations", "Finance", "QHSE", "HR"]
    return render(request, 'home1.html', {'sections': sections})



def home2(request):
	return render(request, 'home2.html', {})

def home3(request, year= datetime.now().year, month= datetime.now().strftime('%B')):
	month = month.capitalize()

	# Convert month from name to number
	month_number= list(calendar.month_name).index(month)
	month_number= int(month_number)

	# Create calendar
	cal = HTMLCalendar().formatmonth(
		year,
		month_number)
	# Get current year
	now = datetime.now()
	current_year = now.year

	# Query the Shipment model for Dates
	shipment_list = Shipment.objects.filter(
	actual_delivery__year= year,
	actual_delivery__month=month_number,	
	)

	# Step 1 Aggregating shipments within the month
	results = Shipment.objects.annotate(
		month=TruncMonth("actual_delivery"),
	).values(
		"month"
	).annotate(
		count=Count("shipment_id"),
		#total_weight=Sum("weight")

	)
	print(results)

	# Step 2 Take the results and parse to the format to be fed to the html page(charts2)
	"""<QuerySet [{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 11, 1), 'count': 1}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 10, 1), 'count': 70}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 9, 1), 'count': 5}]>
  	"""
	month_labels = []
	month_counts = []

	for record in results:
		month_counts.append(record["count"])
		month_labels.append(record["month"].strftime("%B"))

	# Get current time
	time = now.strftime('%H:%M:%S')

	return render(request, 'charts2.html', {
		"months": month_labels,
		"data": month_counts,
		"year": year,
		"month": month,
		"month_number": month_number,
		"cal": cal,
		"current_year": current_year,
		"time": time,
		"shipment_list": shipment_list,
		})

	
def samples(request):
	return render(request, 'samples.html', {})

@login_required
@permission_required("dash_board.can_view_page_hr")
def hr_support(request):
	# Step 1 Aggregating shipments within the month
	results = Shipment.objects.annotate(
		month=TruncMonth("actual_delivery"),
	).values(
		"month"
	).annotate(
		count=Count("shipment_id"),
		#total_weight=Sum("weight")

	).order_by("month")
	print(results)

	# Step 2 Take the results and parse to the format to be fed to the html page(charts2)
	"""<QuerySet [{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 11, 1), 'count': 1}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 10, 1), 'count': 70}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 9, 1), 'count': 5}]>
  	"""
	month_labels = []
	month_counts = []

	for record in results:
		month_counts.append(record["count"])
		month_labels.append(record["month"].strftime("%B"))
	
	return render(request, 'hr_support.html', {
		"months": month_labels,
		"data": month_counts,
	})

@login_required
@permission_required("dash_board.can_view_page_hr")
def operations(request):
	# Step 1 Aggregating shipments within the month
	results = Shipment.objects.annotate(
		month=TruncMonth("actual_delivery"),
	).values(
		"month"
	).annotate(
		count=Count("shipment_id"),
	).order_by("month")
	print(results)

	# Step 2 Take the results and parse to the format to be fed to the html page(charts2)
	"""<QuerySet [{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 11, 1), 'count': 1}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 10, 1), 'count': 70}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 9, 1), 'count': 5}]>
  	"""
	month_labels = []
	month_counts = []

	for record in results:
		month_counts.append(record["count"])
		month_labels.append(record["month"].strftime("%B"))
	
	return render(request, 'operations', {
		"months": month_labels,
		"data": month_counts,
	})
@login_required()
@permission_required("dash_board.can_view_page_ops")
def ops(request):
	print(request.user.is_authenticated)
	print(request.user.has_perm('dash_board.can_view_page_ops'))
	# Step 1 Aggregating shipments within the month
	results = Shipment.objects.annotate(
		month=TruncMonth("actual_delivery"),
	).values(
		"month"
	).annotate(
		count=Count("shipment_id"),
	).order_by("month")
	print(results)

	# Step 2 Take the results and parse to the format to be fed to the html page(charts2)
	"""<QuerySet [{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 11, 1), 'count': 1}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 10, 1), 'count': 70}, 
	{'year': datetime.date(2024, 1, 1), 'month': datetime.date(2024, 9, 1), 'count': 5}]>
  	"""
	month_labels = []
	month_counts = []

	for record in results:
		month_counts.append(record["count"])
		month_labels.append(record["month"].strftime("%B"))

	return render(request, 'ops.html', {
		"months": month_labels,
		"data": month_counts,
	})
	
def add_shipment(request):
	if request.method =='POST':
		form = ShipmentForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, "Shipment has been added")
			return redirect('ops')
		else:
			print(form.errors)
			messages.success(request, "Error")
			return render(request, 'add_shipment.html', {})
		
	else:
		return render(request, 'add_shipment.html', {})

	
def add_bill(request):
	if request.method =='POST':
		form = BillForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, "Bill has been added")
			return redirect('bills')
		else:
			print(form.errors)
			messages.success(request, "Error")
			return render(request, 'add_bill.html', {})
			
		
	else:
		return render(request, 'add_bill.html', {})

def pretrip(request):
	if request.method =='POST':
		form = PretripForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, "Pretrip has been added")
			return redirect('forms')
		else:
			print(form.errors)
			messages.success(request, "Error")
			return render(request, 'pretrip.html', {})
			
		
	else:
		return render(request, 'pretrip.html', {})
	

def waybill(request):
	if request.method == 'POST':
		form = WaybillForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Waybill created successfully!')
			return redirect('waybill') # Redirect to the same page or another page
		else:
			messages.error(request, 'Error creating waybill. Please check the form.')
		
	
	else:
		form = WaybillForm()
	return render(request, 'waybill.html', {'form': form})


def fuelreq(request):
     if request.method == 'POST':
         form = FuelReqForm(request.POST or None)
         if form.is_valid():
             fuel_req = form.save(commit=False)  # Get the instance without saving
             fuel_req.signature = request.POST.get('signature')  # Add the signature data
             fuel_req.save()  # Save the instance with the signature
             messages.success(request, "Fuel Req has been authorized")
             return redirect(reverse('dash_board:forms'))
         else:
             print(form.errors)
             messages.error(request, "Error")
             return render(request, 'fuelreq.html', {'form': form})
     else:
         form = FuelReqForm()
         return render(request, 'fuelreq.html', {'form': form})

def view_signature(request, pk):
	fuel_req = FuelReq.objects.get(pk=pk)
	decoded_signature = fuel_req.get_decoded_signature()
	return render(request, 'template.html', {'decoded_signature': decoded_signature})


	
def edit(request, list_id):
	if request.method =='POST':
		current_shipment = Shipment.objects.get(pk=list_id)
		form = ShipmentForm(request.POST or None, instance=current_shipment)
		if form.is_valid():
			form.save()
			messages.success(request, "Shipment has been edited")
			return redirect('ops.html')
		else:
			messages.success(request, "Error")
			return render(request, 'add_shipment.html', {})
		
	else:
		get_shipment = Shipment.objects.get(pk=list_id)
		return render(request, 'add_shipment.html', {'get_shipment': get_shipment})

def delete(request, list_id):
	if request.method =='POST':
		current_shipment = Shipment.objects.get(pk=list_id)
		current_shipment.delete()
		messages.success(request, "Shipment deleted")
		return redirect ('ops.html')
	else:
		messages.success(request, "Cannot delete from Page")
		return redirect ('add_shipment.html')

@login_required
@permission_required("dash_board.can_view_page_finance")
def finance(request):
	return render(request, 'finance.html', {})

@login_required
@permission_required("dash_board.can_view_page_qhse")
def qhse(request):
	return render(request, 'qhse.html', {})

def upload(request):
	return render(request, 'upload.html', {})

def transport_table(request):
	all_transports = Transport.objects.all()
	return render(request, 'transport_table.html', {'all_transports': all_transports})

def clearing_table(request):
	all_shipments = Shipment.objects.all()
	return render(request, 'dash_board:clearing_table.html', {'all_shipments': all_shipments})

def organization(request):
	return render(request, 'organization.html',{})
def vieworganization(request):
	return render(request, 'vieworganization.html',{})

def shipments(request):
	return render(request, 'shipments.html', {})

def transports(request):
	return render(request, 'transports.html', {})

def charts(request):
	return render(request, 'charts.html', {	})

def add_bl2(request):
	if request.method =='POST':
		form = BillForm2(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, "Bill has been added")
			return redirect('bills')
		else:
			print(form.errors)
			messages.success(request, "Error")
			return render(request, 'add_bl2.html', {})
			
		
	else:
		return render(request, 'add_bl2.html', {})


def transportsView(request):
	jn_no= Transport.objects.filter(booking_id='Job Number').count()
	jn_no= int(jn_no)
	print('Number of Transport Jobs Completed Are',jn_no)

	tw_no= Transport.objects.filter(chargeable_wgt='Total Weight').sum()
	tw_no= int(tw_no)
	print('Total Weight Transported',tw_no)

	cm_no= Transport.objects.filter(first_pick_up_cont_mode='Container Mode').count()
	cm_no= int(cm_no)
	print('Container Mode',cm_no)

	booking_id_list =[]
	chargeable_wt_list=[]
	first_pick_up_cont_mode_list=['FCL', 'LCL', 'Loose']

def bills(request):
	return render(request, 'bills.html', {})

def invoice(request):
		if request.method =='POST':
			form = InvoiceForm(request.POST or None)
			if form.is_valid():
				form.save()
				messages.success(request, "Invoice has been added")
				return redirect('invoice')
			else:
				print(form.errors)
				messages.success(request, "Error")
				return render(request, 'invoice.html', {})
			
		else:
			return render(request, 'invoice.html', {})

def lineitems(request):
		context= {'form': PacklistForm(), 'packlists': Packlist.objects.all()()}
		return render(request, 'lineitems.html', context)


def create_packlist(request):
	if request.method=="POST":
		form = PacklistForm(request.POST or None)
		if form.is_valid():
			packlist= form.save()
			context={'packlist': packlist}
			return render(request, 'partials/plitem.html', context)
	return render(request, 'partials/form.html', {'form': PacklistForm})

def plitem(request):
	return render(request, 'partials/plitem.html', {})

def purchase_order(request):
	return render(request, 'purchase_order.html', {})

def forms(request):
	return render(request, 'forms.html', {})





