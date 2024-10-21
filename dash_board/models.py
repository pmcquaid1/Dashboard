from django.db import models

class Shipment(models.Model):
	shipment_id = models.CharField(max_length= 20)
	consignee = models.CharField(max_length= 200)
	ata = models.CharField(max_length= 50)
	cargo_available = models.CharField(max_length= 50)
	date_cleared = models.CharField(max_length= 50)
	actual_delivery = models.CharField(max_length= 50)
	cont = models.CharField(max_length= 10)
	twenty_ft = models.CharField(max_length= 10)
	forty_ft = models.CharField(max_length= 10)
	uw = models.CharField(max_length= 10)
	weight = models.CharField(max_length= 10)

	def __str__(self): 
		return self.name

