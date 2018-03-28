from django.db import models

# Create your models here.
class User(models.Model):
	name_text = models.CharField(max_length=100)
	password = models.CharField(max_length=200)
	def __str__(self):
		return self.name_text