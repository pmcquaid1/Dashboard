from django.db import models

class Shipment(models.Model):
	shipment_id = models.CharField(max_length= 15)
	consignee = models.CharField(max_length= 25)
	ata = models.DateField()
	cargo_available = models.DateField()
	date_cleared = models.DateField()
	actual_delivery = models.DateField()
	cont = models.CharField(max_length= 10)
	twenty_ft = models.IntegerField()
	forty_ft = models.IntegerField()
	uw = models.CharField(max_length= 10)
	weight = models.IntegerField()

	def __str__(self): 
		return self.shipment_id



