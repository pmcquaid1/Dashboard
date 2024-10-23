from django import forms
from .models import Shipment

class ShipmentForm(forms.ModelForm):
		class Meta:
			model = Shipment
			fields = ["shipment_id", "consignee", "ata", "cargo_available", "date_cleared", "actual_delivery", "cont", "twenty_ft", "forty_ft","uw", "weight",]