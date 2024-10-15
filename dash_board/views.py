from django.shortcuts import render, redirect

def home(request):
	return render(request, 'home.html',{})

def kpi_reports(request):
	return render(request, 'kpi_reports.html',{})


