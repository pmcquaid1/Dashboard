from django.db import models

class Category(models.Model):
	name=models.CharField(max_length= 50, unique=True)
	
	class Meta:
		verbose_name_plural= 'Categories'

def __str__(self): 
		return self.name

class Shipment(models.Model):
	shipment_id = models.CharField(max_length= 50)
	consignee = models.CharField(max_length= 50)
	ata = models.DateField(max_length= 15)
	cargo_available = models.DateField(max_length= 20)
	date_cleared = models.DateField(max_length= 20)
	actual_delivery = models.DateField(max_length= 20)
	cont = models.CharField(max_length= 50)
	twenty_ft = models.CharField(max_length= 50)
	forty_ft = models.CharField(max_length= 50)
	uw = models.CharField(max_length= 50)
	weight = models.CharField(max_length= 50)

	def __str__(self): 
		return self.shipment_id




