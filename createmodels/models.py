from django.db import models


class StoreStatus(models.Model):
	storeid = models.CharField(max_length=150)
	date_utc = models.DateField(auto_now=False)
	time_utc = models.TimeField(auto_now=True)
	status = models.CharField(max_length=150)
    
	def __str__(self):
		return self.storeid
		
class BusinessHours(models.Model):
	storeid = models.CharField(max_length=150)
	dayofweek = models.IntegerField(null=True)
	start_time = models.TimeField(auto_now=False)
	end_time = models.TimeField(auto_now=False)
	
	def __str__(self):
		return self.storeid 
		
class StoreTimezone(models.Model):
	storeid = models.CharField(max_length=150)
	timezone = models.CharField(max_length=150)
	def __str__(self):
		return self.storeid
