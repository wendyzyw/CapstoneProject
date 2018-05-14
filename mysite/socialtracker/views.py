# Python
import oauth2 as oauth
import cgi
import urllib.parse
import time
import json
import tweepy
import calendar
import simplejson
import facebook
from watson_developer_cloud import PersonalityInsightsV3, ToneAnalyzerV3
from watson_developer_cloud import WatsonApiException 
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, KeywordsOptions, ConceptsOptions
  
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
					
def keywords(request):
	return render(request, 'keywords.html')

def tone_analysis(request):
	tone = request.session['tone']
	document_tone = tone['document_tone']
	sentences_tone = tone['sentences_tone']
	
	# build data structure to stores aggregated scores for all 13 tones
	allTones = []
	t1 = {'Id': 1, 'DisplayName': 'Anger', 'category': 'Emotion Tone', 'IndexScore': 0.0, 'AllText': []}
	t2 = {'Id': 2, 'DisplayName': 'Disgust', 'category': 'Emotion Tone', 'IndexScore': 0.0, 'AllText': [] }
	t3 = {'Id': 3, 'DisplayName': 'Fear', 'category': 'Emotion Tone', 'IndexScore': 0.0, 'AllText': [] }
	t4 = {'Id': 4, 'DisplayName': 'Joy', 'category': 'Emotion Tone', 'IndexScore': 0.0, 'AllText': [] }
	t5 = {'Id': 5, 'DisplayName': 'Sadness', 'category': 'Emotion Tone', 'IndexScore': 0.0, 'AllText': [] }
	t6 = {'Id': 6, 'DisplayName': 'Analytical', 'category': 'Language Tone', 'IndexScore': 0.0, 'AllText': []}
	t7 = {'Id': 7, 'DisplayName': 'Confident', 'category': 'Language Tone', 'IndexScore': 0.0, 'AllText': []}
	t8 = {'Id': 8, 'DisplayName': 'Tentative', 'category': 'Language Tone', 'IndexScore': 0.0, 'AllText': []}
	t9 = {'Id': 9, 'DisplayName': 'Openness', 'category': 'Social Tone', 'IndexScore': 0.0, 'AllText': []}
	t10 = {'Id': 10, 'DisplayName': 'Conscientiousness', 'category': 'Social Tone', 'IndexScore': 0.0, 'AllText': []}
	t11 = {'Id': 11, 'DisplayName': 'Extraversion', 'category': 'Social Tone', 'IndexScore': 0.0, 'AllText': []}
	t12 = {'Id': 12, 'DisplayName': 'Agreeableness', 'category': 'Social Tone', 'IndexScore': 0.0, 'AllText': []}
	t13 = {'Id': 13, 'DisplayName': 'Emotional Range', 'category': 'Social Tone', 'IndexScore': 0.0, 'AllText': []}
	allTones.extend([t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13])
	
	# calculate aggregated score for each tone
	for sentence in sentences_tone:
		categories = sentence['tone_categories']
		emotion = categories[0]['tones']
		language = categories[1]['tones']
		social = categories[2]['tones']
		counter1 = 0
		for each in emotion:
			allTones[counter1]['IndexScore'] += each['score']
			counter1 += 1
		counter2 = 5
		for each in language:
			allTones[counter2]['IndexScore'] += each['score']
			counter2 += 1
		counter3 = 8
		for each in social: 
			allTones[counter3]['IndexScore'] += each['score']
			counter3 += 1
	# print(allTones)

	return render(request, 'toneAnalysis.html', { 'tone_data': allTones })
	
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
			
			# format timeline data from twitter for request format to PersonalityInsightsV3 api 
			reqJson = []
			for each in data:
				temp = {'content': each.text, 'contenttype': "text/plain", 'id': each.id, 'language': 'en'}
				reqJson.append(temp)
			json_input = {'contentItems': reqJson}
				
			try:
				###############################################################
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
				request.session['preferences'] = consumption_preferences
				
				###############################################################		
				reqStrList = []
				for each in data:
					reqStrList.append(each.text)
				reqStr = '. '.join(reqStrList)
				
				tone_analyzer = ToneAnalyzerV3(
					version='2016-05-19',
					username='6c984f2f-56ea-4a07-a59c-9c86e5b5d00f',
					password='GlMwVmKrNpwt'
				)
				tone_analyzer.set_default_headers({'x-watson-learning-opt-out': "true"})

				content_type = 'application/json'
				tone = tone_analyzer.tone({"text": reqStr},content_type)

				# print(json.dumps(tone, indent=2))
				request.session['tone'] = tone
				###############################################################
				natural_language_understanding = NaturalLanguageUnderstandingV1(
					  username='fc0c4c4c-a1aa-4428-b624-1d995c7d4183',
					  password='m6QGBRl7hG3w',
					  version='2018-03-16')
				
				response = natural_language_understanding.analyze(
					  text=reqStr,
					   features=Features(
							concepts=ConceptsOptions(
							  limit=10)))
				
				# print(json.dumps(response, indent=2))
				
			except WatsonApiException as ex:
				print("Method failed with status code " + str(ex.code) + ": " + ex.message)

	except:
		twitter_account = None

	return render(request, 'data.html', { 'radarData': radarData })
	
def callapi(request):
	# get friends from twitter
	consumer_key = "hgijLaRwrPerjxst71EjoL04W"
	consumer_secret = "8OSsk0Jl9QB1cf75yrJ6Y6J4kBVuddulLsse6E24soD6yQnYlw"
	access_token = "3307035747-oLrZE09RH0wkeYtQIXlm5aqZ9nZ5X9PKUi7fjhl"
	access_token_secret = "DYrUq9Y0q66TOEnCgZbjgTtCCGYZfM9XSPpAR6ylhtDvh"
	  
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	my_followers = api.followers()
	my_friends = api.friends()
	my = api.me()
	friends = []
	edges = []
	info = dict(nodes=friends, links=edges)
	user = {'id': my.screen_name, 'group': 1}
	twitter_dict = {'id': 'twitter', 'group': 2}
	facebook_dict = {'id': 'facebook', 'group': 3}
	tumblr_dict = {'id':'tumblr','group':6}
	reddit_dict = {'id':'reddit','group':7}
	edges1 = {'source': my.screen_name, 'target': 'facebook', 'value': 2}
	edges2 = {'source': my.screen_name, 'target': 'twitter', 'value': 2}
	edges3 = {'source':my.screen_name,'target':'tumblr','value':2}
	edges4 = {'source':my.screen_name,'target':'reddit','value':2}
	friends.append(twitter_dict)
	friends.append(user)
	friends.append(facebook_dict)
	friends.append(tumblr_dict)
	friends.append(reddit_dict)
	for follower in my_followers:
		for friend in my_friends:
			if friend.id == follower.id:
				temp = {'id': friend.screen_name, 'group': 4}
				friends.append(temp)
	for line in friends:
		if line['id'] != 'facebook' and line['id'] != 'twitter' and line['id'] != my.screen_name and line['id']!='tumblr' and line['id']!='reddit':
			temp2 = {'source': 'twitter', 'target': line['id'], 'value': 2}
			edges.append(temp2)
	edges.append(edges1)
	edges.append(edges2)
	edges.append(edges3)
	edges.append(edges4)
	# get friends from facebook
	token ='EAACEdEose0cBADDDOyNXQ3YVBrUZCmxl1ZBW2ZBjZCvj9VfjGybKfFxW8UUB7VvKgc8dK4AcZClwtllWi9yy49I1I5qth4zAZC5MLsIugHZBNIX9bwuGywnPLryQnHULPTuYPYsZB5FwqG4122k7iNDq7BQeUOqrStlUSyO87v9FHmArbKjpn2AB3tEZAOFimnkBzZAx6KDNdGmwZDZD'
	graph = facebook.GraphAPI(access_token=token)
	facebook_friends = graph.get_connections(id='me', connection_name='friends')
	for post in facebook_friends["data"]:
		temp3 = {'id':post["name"],'group':5}
		friends.append(temp3)
	for post2 in facebook_friends["data"]:
		temp4 = {'source':'facebook','target':post2["name"],'value':2}
		edges.append(temp4)
	# return JsonResponse(info,safe = False)
	return render(request, 'social_network.html', { 'network_info': info })

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
