from django.urls import path
from . import views

app_name= 'website'

urlpatterns = [
    path('', views.home, name="home"),
    path('shipments', views.shipments, name="shipments"),
    path('add_shipment', views.add_shipment, name="add_shipment"),
    path('edit/<list_id>', views.edit, name="edit"),
    path('delete/<list_id>', views.delete, name= "delete"),
    path('samples', views.samples, name= "samples"),
    path('ops', views.ops, name= "ops"),
    path('finance', views.finance, name= "finance"),
    path('qhse', views.qhse, name= "qhse"),
    path('hr_support', views.hr_support, name= "hr_support"),
    
]  
