from django.db import models

class Shipment(models.Model):
	shipment_id = models.CharField(max_length= 15)
	consignee = models.CharField(max_length= 25)
	ata = models.CharField(max_length= 25)
	cargo_available = models.CharField(max_length= 25)
	date_cleared = models.CharField(max_length= 25)
	actual_delivery = models.CharField(max_length= 25)
	cont = models.CharField(max_length= 10)
	twenty_ft = models.CharField(max_length= 25)
	forty_ft = models.CharField(max_length= 25)
	uw = models.CharField(max_length= 10)
	weight = models.CharField(max_length= 25)

	def __str__(self): 
		return self.shipment_id



