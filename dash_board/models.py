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




