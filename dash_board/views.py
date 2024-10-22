from django.shortcuts import render, redirect
from .models import Shipment
from .forms import ShipmentForm
from django.contrib import messages


def home(request):
	all_shipments = Shipment.objects.all
	return render(request, 'home.html', {'all_shipments':all_shipments})

def kpi_reports(request):
	if request.method =='POST':
		form=ShipmentForm(request.POST or None)
		""""
		if form.is_valid():
			form.save()
			messages.success(request, ('Shipment has been added'))
			return redirect('home')
		else:
			messages.success(request, ('Error not saving to database'))
			return render(request, 'kpi_reports.html', {})
		"""
	else:
		return render(request, 'kpi_reports.html', {})


