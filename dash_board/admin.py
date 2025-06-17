from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Shipment, Transport, Waybill, Bill, Organization,
    Invoice, Packlist, FuelReq, Pretrip, Employee
)

@admin.register(Shipment)
@admin.register(Transport)
@admin.register(Bill)
@admin.register(Organization)
@admin.register(Invoice)
@admin.register(Packlist)
@admin.register(FuelReq)
@admin.register(Pretrip)
@admin.register(Waybill)
@admin.register(Employee)
class ViewAdmin(ImportExportModelAdmin):
    pass

