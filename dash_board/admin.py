from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Shipment, Document, Transport, Waybill, Bill, Organization,
    Invoice, Packlist, FuelReq, Pretrip, Employee
)
from .resources import EmployeeResource
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

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
    list_display = (
        'shipment_reference', 'waybill_number', 'event_type',
        'estimated_arrival_date', 'actual_departure_date'
    )
    list_filter = ('event_type', 'transport_mode', 'carrier')
    search_fields = ('shipment_reference', 'waybill_number', 'consignee', 'consignor')
    date_hierarchy = 'estimated_arrival_date'
    ordering = ['-estimated_arrival_date']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('file', 'data_source_key', 'shipment')
    search_fields = ('file', 'data_source_key')
    autocomplete_fields = ['shipment']

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

class CustomGroupAdmin(GroupAdmin):
    def users_in_group(self, obj):
        return ", ".join(user.username for user in obj.user_set.all())
    users_in_group.short_description = "Users"

    list_display = ("name", "users_in_group")

# Unregister default Group admin and register custom one
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
