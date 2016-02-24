from django.db import models

# Create your models here.
class Marker(models.Model):
	title = models.CharField(max_length=30, unique=True);
	latitude = models.DecimalField(max_digits=18, decimal_places=15);
	longitude = models.DecimalField(max_digits=18, decimal_places=15);
	def __unicode__ (self):
		return self.title
