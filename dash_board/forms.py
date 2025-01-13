from django import forms
from .models import Organization
from .models import Shipment
from .models import Bill
from .models import Invoice
from .models import Packlist
from .models import Transport
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User 
from django.utils import timezone

class OrganizationForm(forms.ModelForm):
		class Meta:
			model = Organization
			fields = ["name", "address", "address2", 
						"city", "region", "country", 
						"digital_address","mobile_phone", "main_phone", "email"]
			
class ShipmentForm(forms.ModelForm):
		class Meta:
			model = Shipment
			fields = ["shipment_id", "consignee", "ata", 
						"cargo_available", "date_cleared", "actual_delivery", 
						"cont", "twenty_ft", "forty_ft","uw", "weight",]

class InvoiceForm(forms.ModelForm):
		class Meta:
			model = Invoice
			fields = ["vendor", "invoice_number", "client", "client_po_number", "invoice_date", "currency", 
			 			"goods_description", "gross_weight", "quantity", "price_unit", "total_amount", "incoterms",]

class PacklistForm(forms.ModelForm):
		class Meta:
			model = Packlist
			fields = ["vendor", "reference_number", "client", "client_po_number", "pack_date", 
			 			"goods_description", "net_weight", "quantity", "hscode",]

class BillForm(forms.ModelForm):
		class Meta:
			model = Bill
			fields = ["bl_number", "shipper", "consignee", "notify_party", 
						"vessel", "port_of_loading", "port_of_discharge", "container_quantity1", "container_type1",
						"container_quantity2", "container_type2",
						"package_quantity1", "package_type1", "package_quantity2", "package_type2","kg_weight","m3", "container_number",]

class BillForm2(forms.ModelForm):
		class Meta:
			model = Bill
			fields = ["bl_number", "shipper", "consignee", "notify_party", 
						"vessel", "port_of_loading", "port_of_discharge", "container_quantity1", "container_type1",
						"container_quantity2", "container_type2",
						"package_quantity1", "package_type1", "package_quantity2", "package_type2",
						"kg_weight","m3", "container_number",]

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

#Register New User

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=False)
	first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)
	department = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Department'}), required=False)

	class Meta:
		model = User
		fields =('username', 'first_name', 'last_name','email','password1', 'password2')

#https://github.com/flatplanet/Django-Ecommerce/blob/main/store/forms.py

def __init__(self, *args, **kwargs):
	super(SignUpForm, self).__init__(*args, **kwargs)

	self.fields['username'].widget.attrs['class'] = 'form-control'
	self.fields['username'].widget.attrs['placeholder'] = 'User Name'
	self.fields['username'].label = ''
	self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

	self.fields['password1'].widget.attrs['class'] = 'form-control'
	self.fields['password1'].widget.attrs['placeholder'] = 'Password'
	self.fields['password1'].label = ''
	self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

	self.fields['password2'].widget.attrs['class'] = 'form-control'
	self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
	self.fields['password2'].label = ''
	self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'  

