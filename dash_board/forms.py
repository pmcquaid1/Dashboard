from django import forms
from .models import Shipment

class ShipmentForm(forms.ModelForm):
		class Meta:
			model = Shipment
			fields = ["shipment_id", "consignee", "ata", ]