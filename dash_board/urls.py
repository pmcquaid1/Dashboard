from django.urls import path
from . import views

urlpatterns = [
    path('', views.newhome, name="newhome"),
    path('newhome', views.newhome, name="newhome"),
    path('add_shipment', views.add_shipment, name="add_shipment"),
    path('edit/<list_id>', views.edit, name="edit"),
    path('delete/<list_id>', views.delete, name= "delete"),

]  
