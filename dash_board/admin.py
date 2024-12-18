from django.contrib import admin
from .models import Shipment
from .models import Transport
from .models import Bill
from .models import Organization
from import_export.admin import ImportExportModelAdmin


@admin.register(Shipment)
@admin.register(Transport)
@admin.register(Bill)
@admin.register(Organization)

class ViewAdmin(ImportExportModelAdmin):
	pass
