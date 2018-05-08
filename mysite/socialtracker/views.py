# Python
import oauth2 as oauth
import cgi
import urllib.parse
import time
import json
import tweepy
import calendar
import simplejson
from watson_developer_cloud import PersonalityInsightsV3
from watson_developer_cloud import WatsonApiException

# Django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import logout as logout
from django.contrib.auth import login as twt_login
from django.contrib.auth import authenticate as twt_authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.backends.google import GooglePlusAuth
from social_core.backends.utils import load_backends
from social_django.utils import psa, load_strategy
from social_django.models import UserSocialAuth

# my app
from socialtracker.models import Profile

####################################
# twitter login 
consumer = oauth.Consumer(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
client = oauth.Client(consumer)

# step 1
request_token_url = 'https://api.twitter.com/oauth/request_token'
# step 2
authenticate_url = 'https://api.twitter.com/oauth/authenticate'
# step 3
access_token_url = 'https://api.twitter.com/oauth/access_token'


# primary pages
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
	user = request.user
	twitter_account = None
	twitter_name = None
	twitter_date = None
	facebook_account = None
	facebook_date = None
	facebook_id = None

	try:
		twitter_account = user.social_auth.get(provider='twitter')
		if twitter_account is not None:
			twitter_json = twitter_account.extra_data
			twitter_name = twitter_json['access_token']['screen_name']
			twitter_date = time.strftime('%d/%m/%Y %H:%M:%S', time.gmtime(twitter_json['auth_time']))

	except UserSocialAuth.DoesNotExist:
		twitter_account = None

	try:
		facebook_account = user.social_auth.get(provider='facebook')
		if facebook_account is not None:
			facebook_json = facebook_account.extra_data
			facebook_date = time.strftime('%d/%m/%Y %H:%M:%S', time.gmtime(facebook_json['auth_time']))
			facebook_id = facebook_json['id']
            # get image url
			fb_profile_url = url = "http://graph.facebook.com/%s/picture?type=large" % facebook_id

	except UserSocialAuth.DoesNotExist:
		facebook_account is None

	social_backend = request.session['social_auth_last_login_backend']
	return render(request, 'Manage3_social.html',
					{'social_backend': social_backend, 'twitter_account': twitter_account, 'twitter_date': twitter_date,
					'twitter_name': twitter_name, 'facebook_account': facebook_account, 'facebook_date': facebook_date,
					'facebook_id': facebook_id})
	
def user_personality(request):
	personality = request.session['user_personality']
	sbData = {'name': 'Sources', 'color': "#d8c51d", 'percent': '', 'children': []}
	totalScore = 0.0
	# top level children list 
	for eachPersonality in personality:
		# to hold 5 traits within each personality
		onePersonality = {'name': eachPersonality['name'], 'color': "#d8c51d", 'size': round(eachPersonality['raw_score'],4), 'percent': 0, 'children': []}
		trait1 = eachPersonality['children'][0]
		trait2 = eachPersonality['children'][1]
		trait3 = eachPersonality['children'][2]
		trait4 = eachPersonality['children'][3]
		trait5 = eachPersonality['children'][4]
		totalScore = trait1['raw_score'] + trait2['raw_score'] + trait3['raw_score'] + trait4['raw_score'] + trait5['raw_score']
		child1 = {'name': trait1['name'], 'color': '#d8c51d', 'size': round(trait1['raw_score'],4), 'percentile': round(trait1['percentile'],4), 'percent': round(trait1['raw_score']/totalScore,4)}
		child2 = {'name': trait2['name'], 'color': '#d8c51d', 'size': round(trait2['raw_score'],4), 'percentile': round(trait2['percentile'],4), 'percent': round(trait2['raw_score']/totalScore,4)}
		child3 = {'name': trait3['name'], 'color': '#d8c51d', 'size': round(trait3['raw_score'],4), 'percentile': round(trait3['percentile'],4), 'percent': round(trait3['raw_score']/totalScore,4)}
		child4 = {'name': trait4['name'], 'color': '#d8c51d', 'size': round(trait4['raw_score'],4), 'percentile': round(trait4['percentile'],4), 'percent': round(trait4['raw_score']/totalScore,4)}
		child5 = {'name': trait5['name'], 'color': '#d8c51d', 'size': round(trait5['raw_score'],4), 'percentile': round(trait5['percentile'],4), 'percent': round(trait5['raw_score']/totalScore,4)}
		onePersonality['children'].append(child1)
		onePersonality['children'].append(child2)
		onePersonality['children'].append(child3)
		onePersonality['children'].append(child4)
		onePersonality['children'].append(child5)
		sbData['children'].append(onePersonality)
		totalScore += eachPersonality['raw_score']
	
	sbData['children'][0]['percent'] = round(personality[0]['raw_score']/totalScore,4)
	sbData['children'][1]['percent'] = round(personality[1]['raw_score']/totalScore,4)
	sbData['children'][2]['percent'] = round(personality[2]['raw_score']/totalScore,4)
	sbData['children'][3]['percent'] = round(personality[3]['raw_score']/totalScore,4)
	sbData['children'][4]['percent'] = round(personality[4]['raw_score']/totalScore,4)
	
	return render(request, 'user_personality.html', {'sbData': sbData})

def user_values(request):
	values = request.session['user_values']
	radarObj = []
	for eachValue in values:
		temp = {"axis": eachValue["name"], "value": round(eachValue["raw_score"],2), "percentile": round(eachValue["percentile"],2)}
		radarObj.append(temp)
	print(radarObj)
	radarData = simplejson.dumps(radarObj)

	return render(request, 'user_values.html', { 'radarData': radarData })
					
def data(request):
	user = request.user
	radarData = []
	try:
		twitter_account = user.social_auth.get(provider='twitter')
		if twitter_account is not None:
			twitter_json = twitter_account.extra_data

            # retriev user timeline
			auth = tweepy.OAuthHandler(settings.TWITTER_TOKEN,settings.TWITTER_SECRET)
			auth.set_access_token(twitter_json['access_token']['oauth_token'],twitter_json['access_token']['oauth_token_secret'])
			api = tweepy.API(auth)
			data = api.user_timeline()
			reqJson = []
			for each in data:
				temp = {'content': each.text, 'contenttype': "text/plain", 'id': each.id, 'language': 'en'}
				reqJson.append(temp)
			json_input = {'contentItems': reqJson}
				
			try:
				personality_insights = PersonalityInsightsV3(
					version='2017-10-13',
					username='9576f431-9a16-435e-85d3-d9dcf455969d',
					password='0HOzAgnxjz3d'
				)
				
				profile = personality_insights.profile(
					content=json_input, content_type='application/json',
					raw_scores=True, consumption_preferences=True)
				# print(json.dumps(profile["values"], indent=2))
				
				personality = profile["personality"]
				needs = profile["needs"]
				values = profile["values"]
				# behavior = profile["behavior"]
				# print("h4")
				consumption_preferences = profile["consumption_preferences"]
				
				#format the values data to pipeline for radar chart
				radarObj = []
				for eachNeed in needs:
					temp = {"axis": "Need "+eachNeed["name"], "value": round(eachNeed["raw_score"],2), "percentile": round(eachNeed["percentile"],2)}
					radarObj.append(temp)
				radarData = simplejson.dumps(radarObj)
				
				# store into session
				request.session['user_values'] = values
				request.session['user_needs'] = needs
				request.session['user_personality'] = personality
				
			except WatsonApiException as ex:
				print("Method failed with status code " + str(ex.code) + ": " + ex.message)

	except:
		twitter_account = None

	return render(request, 'data.html', { 'radarData': radarData })


def twitter_login(request):
	# step 1: send req token request to twitter
	resp, content = client.request(request_token_url, "POST")
	if resp['status'] != '200':
		raise Exception("Request token request fail.")

	# step 2: store req tokken in a session
	print("In Log in :")
	print(request.session.items())
	request_token = request.session['request_token'] = dict(urllib.parse.parse_qsl(content.decode("utf-8")))

	# #step 3: redirect to authentication url
	url = "%s?oauth_token=%s" % (authenticate_url, request.session['request_token']['oauth_token'])
	return HttpResponseRedirect(url)


@login_required
def twitter_logout(request):
	logout(request)
	# redirect back to homepage
	return HttpResponseRedirect('/socialtracker')


def twitter_authenticated(request):
	# step 1: use the oauth-token to build new client
	token = oauth.Token(request.session['request_token']['oauth_token'],
						request.session['request_token']['oauth_token_secret'])
	token.set_verifier(request.GET['oauth_verifier'])
	client = oauth.Client(consumer, token)

	# step 2: request the access token from twitter
	resp, content = client.request(access_token_url, "POST")
	if resp['status'] != '200':
		print(content)
		raise Exception("Access token request fail")

	# step 3: store use id with screen name
	access_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))
	try:
		user = User.objects.get(username=access_token['screen_name'])
	except User.DoesNotExist:
		# creat user if not already exist
		user = User.objects.create_user(access_token['screen_name'], '%s@twitter.com' % access_token['screen_name'],
										password=access_token['oauth_token_secret'])
		print("After created")
		print(user)

		profile = Profile()
		profile.user = user
		profile.oauth_token = access_token['oauth_token']
		profile.oauth_secret = access_token['oauth_token_secret']
		profile.save()

	# step 4: authenticate user and log them in
	# auth_user = twt_authenticate(username=access_token['screen_name'],
	# password=access_token['oauth_token_secret'])
	twt_login(request, user, 'django.contrib.auth.backends.ModelBackend')

	# auth = tweepy.OAuthHandler(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
	# auth.set_access_token(access_token['oauth_token'], access_token['oauth_token_secret'])
	# api = tweepy.API(auth)

	# for status in tweepy.Cursor(api.user_timeline, screen_name=access_token['screen_name']).items():
	# print(status._json['text'])

	return HttpResponseRedirect('/socialtracker/account')
