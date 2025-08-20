from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView




urlpatterns = [
    # Test Environment
    path('test_home/', views.test_home, name="test_home"),
    path('ping/', views.ping),
    path('healthcheck/', lambda r: HttpResponse("OK"), name='healthcheck'),
    path('shipment_test/', views.shipment_test, name="shipment_test"),
    path('document_test/', views.document_test, name="document_test"),
    path('routes/', views.list_routes),


    # Core Pages
    path('', views.landing, name="landing"),
    path('base/', views.base, name="base"),
    path('dashboard/', views.dashboard, name="dashboard"),
    #path('home3/', views.home3, name="home3"),
    #path('<int:year>/<str:month>/', views.home3, name="home3"),

    # Dashboard & Modules
    #path('samples/', views.samples, name="samples"),
    path('transport/', views.transport, name="transport"),
    path('c_f/', views.c_f, name="c_f"),
    path('warehouse/', views.warehouse, name="warehouse"),
    path('documentation/', views.documentation, name="documentation"),
    path('finance/', views.finance, name="finance"),
    path('qhse/', views.qhse, name="qhse"),
    path('hr_support/', views.hr_support, name="hr_support"),
    path('revops/', views.revops, name="revops"),
    path('employee/', views.register, name='employee'),
    path('employee/confirmation/', TemplateView.as_view(template_name='employee_confirmation.html'), name='employee_confirmation'),


    # Shipments
    path('add_shipment/', views.add_shipment, name="add_shipment"),
    path('edit/<list_id>/', views.edit, name="edit"),
    path('delete/<list_id>/', views.delete, name="delete"),

    # Tables
    path('clearing_table/', views.clearing_table, name="clearing_table"),
    path('transport_table/', views.transport_table, name="transport_table"),

    # Charts
    path('charts/', views.charts, name="charts"),

    # Forms & Documents
    path('upload/', views.upload, name="upload"),
    path('forms/', views.forms, name="forms"),
    path('forms2/', views.forms2, name="forms2"),
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
    path('fuelreq_sign/<int:pk>/', views.fuelreq_sign, name='fuelreq_sign'),


    # Signature
    path('signature/<int:pk>/', views.signature, name="signature"),
    
    # User Management
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('update_user/', views.update_user, name="update_user"),
    path('update_password/', views.update_password, name="update_password"),
    path('profile/', views.profile, name="profile"),
    path("import_employees/", views.import_employees, name="import_employees"),
    path("import_csv/", views.import_csv, name="import_employees"),
    # Misc
    path('my_view/', views.my_view, name="my_view"),
]


