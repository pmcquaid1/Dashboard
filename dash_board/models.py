from django.db import models


class Organization(models.Model):
	name= models.CharField(max_length= 200)
	address= models.CharField(max_length= 200)
	address2= models.CharField(max_length= 200)
	city= models.CharField(max_length= 100)
	region= models.CharField(max_length= 100)
	country= models.CharField(max_length= 100)
	digital_address= models.CharField(max_length=50)
	mobile_phone= models.Field(max_length=50)
	main_phone= models.CharField(max_length=50)
	email= models.CharField(max_length= 100)

	def __str__(self): 
		return "{}-{}".format(self.name, self.address, 
						self.address2, self.city, self.region, self.country,
						self.digital_address, self.mobile_phone, self.main_phone, self.email)
class Bill(models.Model):
	bl_number= models.CharField(max_length= 20)	
	shipper= models.CharField(max_length= 30)	
	consignee= models.CharField(max_length= 30)
	notify_party= models.CharField(max_length= 30)	
	vessel= models.CharField(max_length= 30)	
	port_of_loading= models.CharField(max_length= 30)	
	port_of_discharge= models.CharField(max_length= 10)	
	container_quantity1= models.IntegerField()	
	container_type1= models.CharField(max_length= 10)
	container_quantity2= models.IntegerField()	
	container_type2= models.CharField(max_length= 10)
	package_quantity1= models.IntegerField()
	package_type1= models.CharField(max_length= 10)	
	package_quantity2= models.IntegerField()
	package_type2= models.CharField(max_length= 10)	
	kg_weight= models.DecimalField(decimal_places=2, max_digits=20)	
	m3= models.DecimalField(decimal_places=2, max_digits=20)
	container_number= models.CharField(max_length= 10)

	
	def __str__(self): 
		return "{}-{}".format(self.bl_number, self.shipper, self.consignee, 
						self.notify_party, self.vessel, self.port_of_loading, self.port_of_discharge,
						self.container_quantity1, self.container_type1, self.container_quantity2, 
						self.container_type2, self.package_quantity1, self.package_type1, self.package_quantity2,
						self.package_type2, self.kg_weight, self.m3, self.container_number)

class Shipment(models.Model):
	shipment_id = models.CharField(max_length= 20)
	consignee = models.CharField(max_length= 30)
	ata = models.DateField()
	cargo_available = models.DateField()
	date_cleared = models.DateField()
	actual_delivery = models.DateField()
	cont = models.CharField(max_length= 20)
	twenty_ft = models.IntegerField()
	forty_ft = models.IntegerField()
	uw = models.CharField(max_length= 10)
	weight = models.DecimalField(decimal_places=2, max_digits=20)
	
	def __str__(self): 
		return "{}-{}".format(self.shipment_id, self.consignee, self.ata, 
						self.cargo_available, self.date_cleared, self.actual_delivery, 
						self.cont, self.twenty_ft, self.forty_ft, self.uw, self.weight)

class Invoice(models.Model):
	vendor = models.CharField(max_length=100)
	invoice_number = models.CharField(max_length= 20)
	client = models.CharField(max_length=100)
	client_po_number = models.CharField(max_length= 20)
	invoice_date = models.DateField(max_length= 30)
	currency = models.DecimalField(decimal_places=2, max_digits=20)
	goods_description = models.CharField(max_length=200)
	gross_weight = models.DecimalField(decimal_places=2, max_digits=20)
	quantity = models.IntegerField()
	price_unit = models.DecimalField(decimal_places=2, max_digits=20)
	total_amount = models.DecimalField(decimal_places=2, max_digits=20)
	incoterms = models.CharField(max_length= 10)
	
	def __str__(self): 
		return "{}-{}".format(self.vendor,self.invoice_number,self.client)

class Transport(models.Model):
	booking_id= models.CharField(max_length= 50)	
	parent_id= models.CharField(max_length= 50)	
	branch= models.CharField(max_length= 50)
	client= models.CharField(max_length= 50)	
	booking_req= models.CharField(max_length= 50)	
	first_pic_actual= models.DateField(max_length= 50)	
	first_pic_city= models.CharField(max_length= 50)	
	last_del_act= models.DateField(max_length= 50)	
	last_del_city= models.CharField(max_length= 50)
	status= models.CharField(max_length= 50)
	hazardous= models.CharField(max_length= 50)
	goods_description= models.CharField(max_length= 50)	
	chargeable_wgt= models.DecimalField(decimal_places=2, max_digits=20)
	chargeable_wgt_unit= models.CharField(max_length= 50)	
	transport= models.CharField(max_length= 50)	
	first_pic_equipment= models.CharField(max_length= 50)
	first_pick_up_cont_mode= models.CharField(max_length= 50)
	first_pu_cont_type= models.CharField(max_length= 50)
	consignee_package_qty= models.IntegerField()
	first_pu_pkg_type= models.CharField(max_length= 50)
	first_pickup_name= models.CharField(max_length= 50)
	booked_by= models.CharField(max_length= 50)

	def __str__(self): 
		return self.booking_id


class Contact(models.Model):
	first_name = models.CharField(max_length= 50)
	last_name = models.CharField(max_length= 50)
	email = models.EmailField(max_length= 50)
	department = models.CharField(max_length= 50)
	
	class Meta:
		# User Permissions to Department Page
		permissions = [
			("can_view_page", "View Page"),
			("can_view_page_ops", "View Ops Page"),
			("can_view_page_finance", "View Finance Page"),
			("can_view_page_qhse", "View QHSE Page"),
			("can_view_page_hr", "View HR Page"),
		] 
	
	def __str__(self): 
		return self.first_name




