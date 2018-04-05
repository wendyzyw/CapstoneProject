#Python 
import oauth2 as oauth
import cgi

#Django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

#my app
from social_analytics.models import Profile

#primary pages 
def index(request):
	return render(request, 'index.html')
	
def login(request):
	return render(request, 'Login.html')

def account(request):
	return render(request, 'account-home.html')
	
def manage1(request):
	return render(request, 'Manage1_privacy.html')

def manage2(request):
	return render(request, 'Manage2_Personal.html')

def manage3(request):
	return render(request, 'Manage3_social.html')
	
def data(request):
	return render(request, 'data.html')

####################################
# twitter login 
consumer = oauth.Consumer(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'

def twitter_login(request):
	return render(request, 'index.html')
	
@login_required
def twitter_authenticated(request):
	return render(request, 'index.html')

def twitter_logout(request):
	return render(request, 'index.html')
