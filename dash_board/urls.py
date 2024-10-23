from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('kpi_reports', views.kpi_reports, name="KPI Reports"),
    path('edit/<list_id>', views.edit, name="edit"),
   
]