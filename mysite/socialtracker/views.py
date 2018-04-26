#Python 
import oauth2 as oauth
import cgi
import urllib.parse
import tweepy

#plotting on data pages
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

#Django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import logout as twt_logout
from django.contrib.auth import login as twt_login
from django.contrib.auth import authenticate as twt_authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

import random
import datetime

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

#my app
from socialtracker.models import Profile

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
	social_backend = request.session['social_auth_last_login_backend']
	return render(request, 'Manage3_social.html',{'social_backend': social_backend})
	
def data(request):
	return render(request, 'data.html')

def radarChart(request):
		# # Set data
	# df = pd.DataFrame({
	# 'group': ['A','B','C','D'],
	# 'var1': [38, 1.5, 30, 4],
	# 'var2': [29, 10, 9, 34],
	# 'var3': [8, 39, 23, 24],
	# 'var4': [7, 31, 33, 14],
	# 'var5': [28, 15, 32, 14]
	# })
	 
	# # number of variable
	# categories=list(df)[1:]
	# N = len(categories)
	 
	# # We are going to plot the first line of the data frame.
	# # But we need to repeat the first value to close the circular graph:
	# values=df.loc[0].drop('group').values.flatten().tolist()
	# values += values[:1]
	# values
	 
	# # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
	# angles = [n / float(N) * 2 * pi for n in range(N)]
	# angles += angles[:1]
	 
	# # Initialise the spider plot
	# ax = plt.subplot(111, polar=True)
	 
	# # Draw one axe per variable + add labels labels yet
	# plt.xticks(angles[:-1], categories, color='grey', size=8)
	 
	# # Draw ylabels
	# ax.set_rlabel_position(0)
	# plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
	# plt.ylim(0,40)
	 
	# # Plot data
	# ax.plot(angles, values, linewidth=1, linestyle='solid')
	 
	# # Fill area
	# ax.fill(angles, values, 'b', alpha=0.1)
	from matplotlib.pyplot import figure, title, bar
	import numpy as np
	import mpld3

	mpl_figure = figure(1, figsize=(6, 6))
	xvalues = range(5)  # the x locations for the groups
	yvalues = np.random.random_sample(5)

	width = 0.5  # the width of the bars    
	bar(xvalues, yvalues, width)
	fig_html = mpld3.fig_to_html(mpl_figure)
	plt.close()

	return render('data.html',
							  {'figure': fig_html, },
							  context_instance = RequestContext(request))


def twitter_login(request):
	#step 1: send req token request to twitter
	resp, content = client.request(request_token_url, "POST")
	if resp['status'] != '200':
		raise Exception("Request token request fail.")
		
	#step 2: store req tokken in a session
	print("In Log in :")
	print(request.session.items())
	request_token = request.session['request_token'] = dict(urllib.parse.parse_qsl(content.decode("utf-8")))
	
	# #step 3: redirect to authentication url
	url = "%s?oauth_token=%s" % (authenticate_url, request.session['request_token']['oauth_token'])
	return HttpResponseRedirect(url)
	
@login_required
def twitter_logout(request):
	print(request.session.items())
	twt_logout(request)
	#redirect back to homepage 
	return HttpResponseRedirect('/socialtracker')
	
def twitter_authenticated(request):
	#step 1: use the oauth-token to build new client
	token = oauth.Token(request.session['request_token']['oauth_token'],
        request.session['request_token']['oauth_token_secret'])
	token.set_verifier(request.GET['oauth_verifier'])
	client = oauth.Client(consumer, token)
	
	#step 2: request the access token from twitter
	resp, content = client.request(access_token_url, "POST")
	if resp['status'] != '200':
		print(content)
		raise Exception("Access token request fail")
	
	#step 3: store use id with screen name
	access_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))
	try: 
		user = User.objects.get(username=access_token['screen_name'])
	except User.DoesNotExist:
		#creat user if not already exist
		user = User.objects.create_user(access_token['screen_name'], '%s@twitter.com' % access_token['screen_name'], password=access_token['oauth_token_secret'])
		print("After created")
		print(user)
		
		profile = Profile()
		profile.user = user
		profile.oauth_token = access_token['oauth_token']
		profile.oauth_secret = access_token['oauth_token_secret']
		profile.save()
		
	#step 4: authenticate user and log them in 
	# auth_user = twt_authenticate(username=access_token['screen_name'],
        # password=access_token['oauth_token_secret'])
	twt_login(request, user, 'django.contrib.auth.backends.ModelBackend')

	# auth = tweepy.OAuthHandler(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
	# auth.set_access_token(access_token['oauth_token'], access_token['oauth_token_secret'])
	# api = tweepy.API(auth)

	# for status in tweepy.Cursor(api.user_timeline, screen_name=access_token['screen_name']).items():
		# print(status._json['text'])
	
	return HttpResponseRedirect('/socialtracker/account')

