from django.shortcuts import render, redirect
from .models import Shipment
from .forms import ShipmentForm
from django.contrib import messages
from .forms import UpdateContact, SignUpForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required

def login_user(request):
	if request.method=="POST":
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
			return redirect('home1')
		
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


	
def samples(request):
	return render(request, 'samples.html', {})

@login_required
@permission_required("dash_board.can_view_page")
def ops(request):
	return render(request, 'ops.html', {})

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
@permission_required("dash_board.can_view_page")
def finance(request):
	return render(request, 'finance.html', {})

@login_required
@permission_required("dash_board.can_view_page")
def qhse(request):
	return render(request, 'qhse.html', {})

@login_required
@permission_required("dash_board.can_view_page")
def hr_support(request):
	return render(request, 'hr_support.html', {})

def upload(request):
	return render(request, 'upload.html', {})

def tables(request):
	all_shipments = Shipment.objects.all
	return render(request, 'tables.html', {'all_shipments': all_shipments})

def shipments(request):
	return render(request, 'shipments.html', {'all_shipments':all_shipments})







