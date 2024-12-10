from calendar import HTMLCalendar
import calendar
from datetime import datetime
from django.shortcuts import render, redirect
from .models import Shipment
from .models import Transport
from .forms import ShipmentForm
from django.contrib import messages
from .forms import UpdateContact, SignUpForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

class ShipmentChartView(TemplateView):
	template_name='charts2.html'
	def get_context_data(self, **kwargs):
		context=super(ShipmentChartView, self).get_context_data(**kwargs)
		context["qs"]= Shipment.objects.all()
		return context

def charts2(request, year, month):
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

	# Get current time
	time = now.strftime('%H:%M:%S')
	return render(request, 'charts2.html', {
		"year": year,
		"month": month,
		"month_number": month_number,
		"cal": cal,
		"current_year": current_year,
		"time": time,
		"shipment_list": shipment_list,
		})


def login_user(request):
	if request.method=="POST":
		#grab form info
		username= request.POST['username']
		password= request.POST['password']
		user= authenticate(request, username=username, password=password)
		print("user:", user.get_all_permissions())

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
	return render(request, 'home1.html', {})


def home2(request):
	return render(request, 'home2.html', {})

def home3(request, year, month):
	name= "Patrick"
	return render(request, 
			   'home3.html', {
				"name": name
				})
	
def samples(request):
	return render(request, 'samples.html', {})

@login_required()
@permission_required("dash_board.can_view_page_ops")
def ops(request):
	return render(request, 'ops.html' )
	
def add_shipment(request):
	if request.method =='POST':
		form = ShipmentForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, "Shipment has been added")
			return redirect('ops.html')
		else:
			messages.success(request, "Error")
			return render(request, 'add_shipment.html', {})
		
	else:
		return render(request, 'add_shipment.html', {})

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

@login_required
@permission_required("dash_board.can_view_page_hr")
def hr_support(request):
	return render(request, 'hr_support.html', {})

def upload(request):
	return render(request, 'upload.html', {})

def transport_table(request):
	all_transports = Transport.objects.all
	return render(request, 'transport_table.html', {'all_transports': all_transports})

def clearing_table(request):
	all_shipments = Shipment.objects.all
	return render(request, 'clearing_table.html', {'all_shipments': all_shipments})

def shipments(request):
	return render(request, 'shipments.html', {})

def transports(request):
	return render(request, 'transports.html', {})

def charts(request):
	labels = []
	data = []
	
	queryset = Shipment.objects.order_by('shipment_id')
	
	for shipment in queryset:
		labels.append(shipment.actual_delivery)
		data.append(shipment.shipment_id)

	return render(request, 'charts.html', {
		'labels': labels,
		'data': data
	})


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







