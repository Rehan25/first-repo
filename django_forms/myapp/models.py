from django.db import models

class Django(models.Model):
	name = models.CharField(max_length=100)
	body = models.TextField()

	def __str__(self):
		return self.name
# Create your models here.
