from django.shortcuts import render, redirect
from .models import Shipment
from .forms import ShipmentForm
from django.contrib import messages


def home(request):
	return render(request, 'home.html', {})
	

def shipments(request):
	all_shipments = Shipment.objects.all
	return render(request, 'shipments.html', {'all_shipments':all_shipments})


def add_shipment(request):
	if request.method =='POST':
		form = ShipmentForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ('Shipment has been added'))
			return redirect('shipments')
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
			return redirect('shipments')
		else:
			messages.success(request, ('Error'))
			return render(request, 'edit.html', {})
		
	else:
		get_shipment = Shipment.objects.get(pk=list_id)
		return render(request, 'edit.html', {'get_shipment': get_shipment})

def delete(request, list_id):
	if request.method =='POST':
		current_shipment = Shipment.objects.get(pk=list_id)
		current_shipment.delete()
		messages.success(request, ('Shipment deleted'))
		return redirect ('shipments')
	else:
		messages.success(request, ('Cannot delete from Page'))
		return redirect ('shipments')


