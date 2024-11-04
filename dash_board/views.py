from django.shortcuts import render, redirect
from .models import Shipment
from .forms import ShipmentForm
from django.contrib import messages


def home2(request):
	return render(request, 'website/home2.html', {})
	
def samples(request):
	return render(request, 'website/samples.html', {})

def ops(request):
	all_shipments = Shipment.objects.all
	return render(request, 'website/ops.html', {'all_shipments': all_shipments})

def add_shipment(request):
	if request.method =='POST':
		form = ShipmentForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ('Shipment has been added'))
			return redirect('website/ops.html')
		else:
			messages.success(request, ('Error'))
			return render(request, 'website/add_shipment.html', {})
		
	else:
		return render(request, 'website/add_shipment.html', {})

def edit(request, list_id):
	if request.method =='POST':
		current_shipment = Shipment.objects.get(pk=list_id)
		form = ShipmentForm(request.POST or None, instance=current_shipment)
		if form.is_valid():
			form.save()
			messages.success(request, ('Shipment has been edited'))
			return redirect('website/ops.html')
		else:
			messages.success(request, ('Error'))
			return render(request, 'website/add_shipment.html', {})
		
	else:
		get_shipment = Shipment.objects.get(pk=list_id)
		return render(request, 'website/add_shipment.html', {'get_shipment': get_shipment})

def delete(request, list_id):
	if request.method =='POST':
		current_shipment = Shipment.objects.get(pk=list_id)
		current_shipment.delete()
		messages.success(request, ('Shipment deleted'))
		return redirect ('website/ops.html')
	else:
		messages.success(request, ('Cannot delete from Page'))
		return redirect ('website/add_shipment.html')
	
def finance(request):
	return render(request, 'website/finance.html', {})

def qhse(request):
	return render(request, 'website/qhse.html', {})

def hr_support(request):
	return render(request, 'website/hr_support.html', {})

def upload(request):
	return render(request, 'website/upload.html', {})

def shipments(request):
	return render(request, 'shipments.html', {'all_shipments':all_shipments})





