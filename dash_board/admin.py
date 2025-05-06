from django.contrib import admin
from .models import Shipment
from .models import Transport
from .models import Waybill
from .models import Bill
from .models import Organization
from .models import Invoice
from .models import Packlist
from .models import FuelReq
from .models import Pretrip
from import_export.admin import ImportExportModelAdmin


@admin.register(Shipment)
@admin.register(Transport)
@admin.register(Bill)
@admin.register(Organization)
@admin.register(Invoice)
@admin.register(Packlist)
@admin.register(FuelReq)
@admin.register(Pretrip)
@admin.register(Waybill)
class ViewAdmin(ImportExportModelAdmin):
	pass
