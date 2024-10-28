from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('shipments', views.shipments, name="shipments"),
    path('add_shipment', views.add_shipment, name="add_shipment"),
    path('edit/<list_id>', views.edit, name="edit"),
    path('delete/<list_id>', views.delete, name= "delete"),

]  
