from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add_shipment', views.add_shipment, name="Shipment"),
    path('edit/<list_id>', views.edit, name="edit"),
   
]