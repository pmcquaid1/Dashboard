from django.db import models

class Shipment(models.Model):
	shipment_id = models.CharField(max_length= 15)
	consignee = models.CharField(max_length= 25)
	ata = models.DateField()
	cargo_available = models.DateField()
	date_cleared = models.DateField()
	actual_delivery = models.DateField()
	cont = models.CharField(max_length= 5)
	twenty_ft = models.IntegerField(max_length= 10)
	forty_ft = models.IntegerField(max_length= 10)
	uw = models.CharField(max_length= 5)
	weight = models.IntegerField(max_length= 10)

	def __str__(self): 
		return self.shipment_id



