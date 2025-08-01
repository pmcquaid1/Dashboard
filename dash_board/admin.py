from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Shipment, Transport, Waybill, Bill, Organization,
    Invoice, Packlist, FuelReq, Pretrip, Employee
)
from .resources import EmployeeResource

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource
    list_display = ("first_name", "last_name", "email", "department", "position", "phone", "location")
    search_fields = ("first_name", "last_name", "email", "department")

    def import_action(self, request, *args, **kwargs):
        print("🔄 Custom import_action triggered in EmployeeAdmin")
        return super().import_action(request, *args, **kwargs)

    def export_action(self, request, *args, **kwargs):
        print("📤 Custom export_action triggered in EmployeeAdmin")
        return super().export_action(request, *args, **kwargs)

    
# 🚚 Register other models using decorators
@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    pass

@admin.register(Waybill)
class WaybillAdmin(admin.ModelAdmin):
    pass

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    pass

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Packlist)
class PacklistAdmin(admin.ModelAdmin):
    pass

@admin.register(FuelReq)
class FuelReqAdmin(admin.ModelAdmin):
    pass

@admin.register(Pretrip)
class PretripAdmin(admin.ModelAdmin):
    pass

