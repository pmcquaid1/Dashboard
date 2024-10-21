from django.shortcuts import render, redirect
from .models import Shipment
from django.contrib import messages


def home(request):
	all_shipments = Shipment.objects.all
	return render(request, 'home.html',{'all_shipments':all_shipments})

def kpi_reports(request):
	return render(request, 'kpi_reports.html',{})


