from django.contrib import admin
from .models import Shipment
from .models import Transport
from .models import Bill
from .models import Organization
from .models import Invoice
from .models import Packlist
from import_export.admin import ImportExportModelAdmin


@admin.register(Shipment)
@admin.register(Transport)
@admin.register(Bill)
@admin.register(Organization)
@admin.register(Invoice)
@admin.register(Packlist)

class ViewAdmin(ImportExportModelAdmin):
	pass
