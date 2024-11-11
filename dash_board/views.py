from django.shortcuts import render, redirect
from .models import Shipment
from .forms import ShipmentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def login_user(request):
	if request.method=="POST":
		username= request.POST['username']
		password= request.POST['password']
		user= authenticate(request, username=username, password=password)
		if user is not None:
			login(request,user)
			messages.success(request, ('User Login Succssful'))
			return redirect('home2')
		
		else:
			messages.success(request, "Login Unsuccesful")
			return redirect('login')
	else:
		return render(request, 'login', {})

def logout_user(request):
	pass

def register_user(request):
	return render(request, 'register.html', {})	

def home2(request):
	return render(request, 'home2.html', {})
	
def samples(request):
	return render(request, 'samples.html', {})

def ops(request):
	return render(request, 'ops.html', {})

def add_shipment(request):
	if request.method =='POST':
		form = ShipmentForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ('Shipment has been added'))
			return redirect('ops.html')
		else:
			messages.success(request, ('Error'))
			return render(request, 'add_shipment.html', {})
		
	else:
		return render(request, 'add_shipment.html', {})

def edit(request, list_id):
	if request.method =='POST':
		current_shipment = Shipment.objects.get(pk=list_id)
		form = ShipmentForm(request.POST or None, instance=current_shipment)
		if form.is_valid():
			form.save()
			messages.success(request, ('Shipment has been edited'))
			return redirect('ops.html')
		else:
			messages.success(request, ('Error'))
			return render(request, 'add_shipment.html', {})
		
	else:
		get_shipment = Shipment.objects.get(pk=list_id)
		return render(request, 'add_shipment.html', {'get_shipment': get_shipment})

def delete(request, list_id):
	if request.method =='POST':
		current_shipment = Shipment.objects.get(pk=list_id)
		current_shipment.delete()
		messages.success(request, ('Shipment deleted'))
		return redirect ('ops.html')
	else:
		messages.success(request, ('Cannot delete from Page'))
		return redirect ('add_shipment.html')
	
def finance(request):
	return render(request, 'finance.html', {})

def qhse(request):
	return render(request, 'qhse.html', {})

def hr_support(request):
	return render(request, 'hr_support.html', {})

def upload(request):
	return render(request, 'upload.html', {})

def tables(request):
	all_shipments = Shipment.objects.all
	return render(request, 'tables.html', {'all_shipments': all_shipments})

def shipments(request):
	return render(request, 'shipments.html', {'all_shipments':all_shipments})







