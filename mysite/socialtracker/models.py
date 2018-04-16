from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
	name_text = models.CharField(max_length=100)
	password = models.CharField(max_length=200)
	def __str__(self):
		return self.name_text

#each user can has many social profiles including the one used for logging in 
class Profile(models.Model):
	user = models.ForeignKey('User',on_delete=models.CASCADE)
	oauth_token = models.CharField(max_length=200, blank=True, null=True, editable=False)
	oauth_secret = models.CharField(max_length=200)
	profile_image_url = models.URLField(max_length=100, blank=True, null=True)