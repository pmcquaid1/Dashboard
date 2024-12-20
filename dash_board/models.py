from django.db import models



class Shipment(models.Model):
	shipment_id = models.CharField(max_length= 50)
	consignee = models.CharField(max_length= 50)
	ata = models.DateField()
	cargo_available = models.DateField()
	date_cleared = models.DateField()
	actual_delivery = models.DateField()
	cont = models.CharField(max_length= 50)
	twenty_ft = models.CharField(max_length= 50)
	forty_ft = models.CharField(max_length= 50)
	uw = models.CharField(max_length= 50)
	weight = models.CharField(max_length= 50)

	
	def __str__(self): 
		return self.shipment_id

class Transport(models.Model):
	booking_id= models.CharField(max_length= 50)	
	parent_id= models.CharField(max_length= 50)	
	branch= models.CharField(max_length= 50)
	client= models.CharField(max_length= 50)	
	booking_req= models.CharField(max_length= 50)	
	first_pic_actual= models.CharField(max_length= 50)	
	first_pic_city= models.CharField(max_length= 50)	
	last_del_act= models.CharField(max_length= 50)	
	last_del_city= models.CharField(max_length= 50)
	status= models.CharField(max_length= 50)
	hazardous= models.CharField(max_length= 50)
	goods_description= models.CharField(max_length= 50)	
	chargeable_wgt= models.CharField(max_length= 50)
	chargeable_wgt_unit= models.CharField(max_length= 50)	
	transport= models.CharField(max_length= 50)	
	first_pic_equipment= models.CharField(max_length= 50)
	first_pick_up_cont_mode= models.CharField(max_length= 50)
	first_pu_cont_type= models.CharField(max_length= 50)
	consignee_package_qty= models.CharField(max_length= 50)
	first_pu_pkg_type= models.CharField(max_length= 50)
	first_pickup_name= models.CharField(max_length= 50)
	booked_by= models.CharField(max_length= 50)

	
	def __str__(self): 
		return self.booking_id


class Contact(models.Model):
	first_name = models.CharField(max_length= 50)
	last_name = models.CharField(max_length= 50)
	email = models.CharField(max_length= 50)
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




