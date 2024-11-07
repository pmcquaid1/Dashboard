from django.contrib import admin
from .models import Shipment
from import_export.admin import ImportExportModelAdmin


@admin.register(Shipment)


class ViewAdmin(ImportExportModelAdmin):
	pass
