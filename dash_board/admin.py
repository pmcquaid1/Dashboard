from django.contrib import admin
from .models import Shipment
from .models import Transport
from import_export.admin import ImportExportModelAdmin


@admin.register(Shipment)
@admin.register(Transport)

class ViewAdmin(ImportExportModelAdmin):
	pass
