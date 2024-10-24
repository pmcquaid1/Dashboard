from django.shortcuts import render, redirect
from .models import Shipment
from .forms import ShipmentForm
from django.contrib import messages


def home(request):
	all_shipments = Shipment.objects.all
	return render(request, 'home.html', {'all_shipments':all_shipments})

def kpi_reports(request):
	if request.method =='POST':
		form = ShipmentForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ('Shipment has been added'))
			return redirect('home')
		else:
			messages.success(request, ('Error'))
			return render(request, 'add_shipment.html', {})
		
	else:
		return render(request, 'add_shipment.html', {})

def edit(request, list_id):
	if request.method =='POST':
		current_shipment = Shipment.objects.get(pk=list_id)
		form = ShipmentForm(request.POST or None, instance= current_shipment)
		if form.is_valid():
			form.save()
			messages.success(request, ('Shipment has been edited'))
			return redirect('home')
		else:
			messages.success(request, ('Error'))
			return render(request, 'edit', {})
		
	else:
		get_shipment = Shipment.objects.get(pk=list_id)
		return render(request, 'edit.html', {'get_shipment': get_shipment})