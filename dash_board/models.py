from django.db import models

class Shipment(models.Model):
	shipmentid = models.CharField(max_length= 20)
	consignee = models.CharField(max_length= 200)
	ata = models.CharField(max_length= 50)
	cargoavailable = models.CharField(max_length= 50)
	datecleared = models.CharField(max_length= 50)
	actualdelivery = models.CharField(max_length= 50)
	cont = models.CharField(max_length= 10)
	twentyft = models.CharField(max_length= 10)
	fortyft = models.CharField(max_length= 10)
	uw = models.CharField(max_length= 10)
	weight = models.CharField(max_length= 10)

	def __str__(self):
		return self.Shipment

