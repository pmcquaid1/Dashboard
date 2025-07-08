from django import forms
from .models import Organization
from .models import Shipment
from .models import Bill
from .models import Invoice
from .models import Packlist
from .models import FuelReq
from .models import Pretrip
from .models import Waybill
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User 
from django.utils import timezone
from .models import Employee  # Make sure this is your updated Employee model with OneToOneField to User

class OrganizationForm(forms.ModelForm):
		class Meta:
			model = Organization
			fields = ["org_type","name", "address", "address2", 
						"city", "region", "country", 
						"digital_address","email"]

class PretripForm(forms.ModelForm):
		class Meta:
			model = Pretrip
			fields = ["driver_name", "vehicle_number", "date", "start_time", 
						"end_time", "odometer_start", "odometer_end", 
						"fuel_start", "fuel_end", "fuel_used", "fuel_cost", 
						"driver_signature", "supervisor_signature", "remarks",]
			
class ShipmentForm(forms.ModelForm):
		class Meta:
			model = Shipment
			fields = ["shipment_id", "transport_mode", "consignee", "ata", 
						"cargo_available", "date_cleared", "actual_delivery", 
						"cont", "twenty_ft", "forty_ft","uw", "weight",]

class InvoiceForm(forms.ModelForm):
		class Meta:
			model = Invoice
			fields = ["vendor", "invoice_number", "client", "client_po_number", "invoice_date", "currency", 
			 			"goods_description", "gross_weight", "quantity", "price_unit", "total_amount", "incoterms",]


class FuelReqForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'id': 'id_date'
        })
    )

    class Meta:
        model = FuelReq
        fields = [
            'date', 'vendor', 'po_number', 'driver_name', 'vehicle_number',
            'place_of_loading', 'destination', 'fuel_quantity', 'initial_tank_amount',
            'top_up_quantity', 'authorized_by'
        ]
        widgets = {
            'vendor': forms.TextInput(attrs={'class': 'form-control'}),
            'po_number': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_name': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control'}),
            'place_of_loading': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'fuel_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'initial_tank_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'top_up_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'authorized_by': forms.TextInput(attrs={'class': 'form-control'}),
        }
		
class WaybillForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Waybill
        fields = [
            'date', 'branch', 'client', 'booking_req', 'transport_ref', 'booking_id', 'parent_id', 'first_pick_up_name', 'first_pic_equipment',
            'first_pic_actual', 'first_pic_city', 'last_del_act', 'last_del_city', 'hazardous', 'goods_description',
            'chargeable_wgt', 'chargeable_wgt_unit', 'transport', 'first_pic_up_cont_mode',
            'first_pu_cont_type', 'consignee_package_qty', 'first_pu_pkg_type'
        ]
        labels = {
            'date': 'Date',
            'branch': 'Branch',
            'client': 'Client',
            'booking_req': 'Request Date',
            'transport_ref': 'PO #',
            'booking_id': 'Transport Booking #',
            'parent_id': 'Shipment #',
            'first_pick_up_name': 'Driver Name',
            'first_pic_equipment': 'Truck #',
            'first_pic_actual': 'Pick up Date',
            'first_pic_city': 'Origin',
            'last_del_act': 'Delivery Date',
            'last_del_city': 'Destination',
            'hazardous': 'Hazardous',
            'goods_description': 'Goods Description',
            'chargeable_wgt': 'Chargeable Weight',
            'chargeable_wgt_unit': 'Chargeable Weight Unit',
            'transport': 'Transport',
            'first_pic_up_cont_mode': 'First Pick-Up Container Mode',
            'first_pu_cont_type': 'First Pick-Up Container Type',
            'consignee_package_qty': 'Consignee Package Quantity',
            'first_pu_pkg_type': 'First Pick-Up Package Type'
        }



class PacklistForm(forms.ModelForm):
		class Meta:
			model = Packlist
			fields = ["vendor", "reference_number", "client", "client_po_number", "pack_date", 
			 			"goods_description", "net_weight", "quantity", "hscode",]
			
			widgets= {
				"vendor": forms.TextInput(attrs={'class': 'form-control'}),
				"reference_number": forms.TextInput(attrs={'class': 'form-control'}),
				"client": forms.TextInput(attrs={'class': 'form-control'}),
				"client_po_number": forms.TextInput(attrs={'class': 'form-control'}),
				"pack_date": forms.TextInput(attrs={'class': 'form-control'}),
				"goods_description": forms.TextInput(attrs={'class': 'form-control'}),
				"net_weight": forms.TextInput(attrs={'class': 'form-control'}),
				"quantity": forms.TextInput(attrs={'class': 'form-control'}),
				"hscode": forms.TextInput(attrs={'class': 'form-control'}),
			 }

class BillForm(forms.ModelForm):
		class Meta:
			model = Bill
			fields = ["bl_number", "shipper", "consignee", "notify_party", 
						"vessel", "port_of_loading", "port_of_discharge", "container_quantity1", "container_type1",
						"container_quantity2", "container_type2",
						"package_quantity1", "package_type1", "package_quantity2", "package_type2","kg_weight","m3", "container_number",]

class UpdateUserForm(UserChangeForm):
	password = None
	first_name = forms.CharField(label="", max_length= 100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)

	class Meta:
		model = User
		fields =('username', 'first_name', 'last_name','email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'


class UpdateContact(forms.ModelForm):
	first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)




class EmployeeForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True
    )
    first_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        required=True
    )
    last_name = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        required=True
    )
    department = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
        required=True
    )
    position = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].label = ''


#https://github.com/flatplanet/Django-Ecommerce/blob/main/store/forms.py

  