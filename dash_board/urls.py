from django.urls import path
from .import views
from dash_board.views import ShipmentChartView

app="dash_board"

urlpatterns = [
    path('', views.home2, name="home2"),
    path('home1', views.home1, name="home1"),
    path('samples', views.samples, name= "samples"),
    path('ops', views.ops, name= "ops"),
    path('finance', views.finance, name= "finance"),
    path('qhse', views.qhse, name= "qhse"),
    path('upload', views.upload, name= "upload"),
    path('hr_support', views.hr_support, name= "hr_support"),
    path('shipments', views.shipments, name="shipments"),
    path('add_shipment', views.add_shipment, name="add_shipment"),
    path('edit/<list_id>', views.edit, name="edit"),
    path('delete/<list_id>', views.delete, name= "delete"),
    path('clearing_table', views.clearing_table, name= "clearing_table"),
    path('transport_table', views.transport_table, name= "transport_table"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
    path('register', views.register_user, name="register"),
    path('update_user', views.update_user, name="update_user"),
    path('update_password', views.update_password, name="update_password"),
    path('home2', views.home2, name="home2"),
    path('charts', views.charts, name= "charts"),
    path('charts2', ShipmentChartView.as_view(), name='charts2'),
    path('<int:year>/<str:month>/', views.calendar, name= "calendar"),


  



]
