from django.db import models

class Shipment(models.Model):
	shipment_id = models.CharField(max_length= 15)
	consignee = models.CharField(max_length= 25)
	ata = models.DateField(max_length= 50)
	cargo_available = models.DateField(max_length= 50)
	date_cleared = models.DateField(max_length= 50)
	actual_delivery = models.DateField(max_length= 50)
	cont = models.CharField(max_length= 10)
	twenty_ft = models.IntegerField(max_length= 10)
	forty_ft = models.IntegerField(max_length= 10)
	uw = models.CharField(max_length= 10)
	weight = models.IntegerField(max_length= 10)

	def __str__(self): 
		return self.shipment_id



