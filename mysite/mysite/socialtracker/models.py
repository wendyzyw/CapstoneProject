from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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
	oauth_secret = models.CharField(max_length=200	)
	profile_image_url = models.URLField(max_length=100, blank=True, null=True)
	social_id = models.CharField(max_length=200, blank=True, null=True)
	social_email = models.CharField(max_length=200, blank=True, null=True)
	social_usename = models.CharField(max_length=200, blank=True, null=True)
	# social_post

class TwitterProfile(models.Model):
	tw_user = models.ForeignKey('User',on_delete=models.CASCADE)
	oauth_token = models.CharField(max_length=200, blank=True, null=True, editable=False)
	oauth_secret = models.CharField(max_length=200	)
	tw_image_url = models.URLField(max_length=100, blank=True, null=True)
	tw_id = models.CharField(max_length=200, blank=True, null=True)
	# tw_email = models.CharField(max_length=200, blank=True, null=True)
	tw_username = models.CharField(max_length=200, blank=True, null=True)

class FacebookProfile(models.Model):
	fb_user = models.ForeignKey('User',on_delete=models.CASCADE)
	fb_id = models.CharField(max_length=200, blank=True, null=True)
	fb_email = models.CharField(max_length=200, blank=True, null=True)
	fb_access_token = models.CharField(max_length=200, blank=True, null=True)
	
