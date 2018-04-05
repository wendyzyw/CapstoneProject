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

def signup(request):
	return render(request, 'signup.html')
	
def forgetPw(request):
	return render(request, 'forget_password.html')

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

#step 1 
request_token_url = 'https://api.twitter.com/oauth/request_token'
#step 2
authenticate_url = 'https://api.twitter.com/oauth/authenticate'
#step 3
access_token_url = 'https://api.twitter.com/oauth/access_token'


def twitter_login(request):
	#step 1: send req token request to twitter
	resp, content = client.request(request_token_url, "GET")
	if resp['status'] != '200':
		raise Excpeption("Request token request fail.")
	#step 2: store req tokken in a session
	request.session['request_token'] = dict(cgi.parse_qsl(content))
	#step 3: redirect to authentication url
	url = "%s?oauth_token=%s" % (authenticate_url, request.session['request_token']['oauth_token'])
	
	return HttpResponseRedirect(url)
	# return render(request, 'index.html')
	
@login_required
def twitter_authenticated(request):
	#step 1: use the oauth-token to build new client
	token = oauth.Token(request.session['request_token']['oauth_token'], request.session['request_token']['oauth_token_secret'])
	token.set_verifier(request.GET['oauth_verifier'])
	client.oauth.Client(consumer, token)
	
	#step 2: request the access token from twitter
	resp, content = client.request(access_token_url, "GET")
	if resp['status'] != '200':
		print(content)
		raise Exception("Access token request fail")
	
	#step 3: store use id with screen name
	access_token = dict(cgi.parse_qsl(content))
	try: 
		use = User.objects.get(username=access_token['screen_name'])
	except User.DoesNotExist:
		#creat user if not already exist
		user = User.objects.create_user(access_token['screen_name'], '%s@twitter.com' % access_token['screen_name'], access_token['oauth_token_secret'])
		
		profile = Profile()
		profile.user = user
		profile.oauth_token = access_token['oauth_token']
		profile.oauth_secret = access_token['oauth_token_secret']
		profile.save()
		
	#step 4: authenticate user and log them in 
	user = authenticate(username=access_token['screen_name'],
        password=access_token['oauth_token_secret'])
	login(request, user)
	
	return HttpResponseRedirect('/account')


def twitter_logout(request):
	logout(request)
	#redirect back to homepage 
	return render(request, 'index.html')
