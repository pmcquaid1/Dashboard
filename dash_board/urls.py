from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from dash_board.views import ShipmentChartView, view_signature
from .views import employee
from django.views.generic import TemplateView

urlpatterns = [
    # Core Pages
    path('', views.home2, name="home2"),
    path('base/', views.base, name="base"),
    path('home/', views.home, name="home"),
    path('home1/', views.home1, name="home1"),
    path('home3/', views.home3, name="home3"),
    path('<int:year>/<str:month>/', views.home3, name="home3"),

    # Dashboard & Modules
    path('samples/', views.samples, name="samples"),
    path('ops/', views.ops, name="ops"),
    path('operations/', views.operations, name="operations"),
    path('finance/', views.finance, name="finance"),
    path('qhse/', views.qhse, name="qhse"),
    path('hr_support/', views.hr_support, name="hr_support"),
    path('employee/', views.employee, name='employee'),
    path('employee/confirmation/', TemplateView.as_view(template_name='employee_confirmation.html'), name='employee_confirmation'),

    # Shipments
    path('shipments/', views.shipments, name="shipments"),
    path('add_shipment/', views.add_shipment, name="add_shipment"),
    path('edit/<list_id>/', views.edit, name="edit"),
    path('delete/<list_id>/', views.delete, name="delete"),

    # Tables
    path('clearing_table/', views.clearing_table, name="clearing_table"),
    path('transport_table/', views.transport_table, name="transport_table"),

    # Charts
    path('charts/', views.charts, name="charts"),
    path('charts2/', ShipmentChartView.as_view(), name="charts2"),

    # Forms & Documents
    path('upload/', views.upload, name="upload"),
    path('forms/', views.forms, name="forms"),
    path('invoice/', views.invoice, name="invoice"),
    path('lineitems/', views.lineitems, name="lineitems"),
    path('create_packlist/', views.create_packlist, name="create_packlist"),
    path('purchase_order/', views.purchase_order, name="purchase_order"),
    path('add_bl2/', views.add_bl2, name="add_bl2"),

    # Bills & Pretrip
    path('bills/', views.bills, name="bills"),
    path('add_bill/', views.add_bill, name="add_bill"),
    path('pretrip/', views.pretrip, name="pretrip"),
    path('waybill/', views.waybill, name="waybill"),

    # Organization
    path('organization/', views.organization, name="organization"),
    path('vieworganization/', views.vieworganization, name="vieworganization"),
    path('detail/<int:id>/', views.detail_view, name="detail_view"),

    # Transport
    path('transport_job_detail/', views.transport_job_detail, name="transport_job_detail"),
    path('fuelreq/', views.fuelreq, name="fuelreq"),

    # Signature
    path('signature/<int:pk>/', view_signature, name="view_signature"),

    # User Management
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('update_user/', views.update_user, name="update_user"),
    path('update_password/', views.update_password, name="update_password"),
    path('profile/', views.profile, name="profile"),

    # Misc
    path('my_view/', views.my_view, name="my_view"),
]

