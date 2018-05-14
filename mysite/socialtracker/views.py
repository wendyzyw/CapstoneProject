# COMP90044 Distributed Computing Project
# Web-based mental analytics app on social media
# Author: Xin Wang, Yiwen Zeng, Yu Han, Chenxi Hou
# Created on: 03/2018

# Python Import
import oauth2 as oauth
import urllib.parse
import time
import simplejson
import tweepy
import requests
from datetime import datetime
from watson_developer_cloud import PersonalityInsightsV3
from watson_developer_cloud import WatsonApiException

# Django Import
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import logout as twt_logout, login as twt_login, update_session_auth_hash
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordChangeView, \
    PasswordResetDoneView, PasswordChangeDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Social_Django Import
from social_django.models import UserSocialAuth

# App Import
from .forms import LoginForm, ChangepassForm, EdituserinfoForm, RegisterForm, MyPasswordResetForm
from .models import UserInfo, TwitterProfile, FackbookProfile, GithubProfile

# Create your views here.


# app name
app_name = 'socialtracker'
# twitter login authentication
consumer = oauth.Consumer(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
client = oauth.Client(consumer)

# step 1
request_token_url = 'https://api.twitter.com/oauth/request_token'
# step 2
authenticate_url = 'https://api.twitter.com/oauth/authenticate'
# step 3
access_token_url = 'https://api.twitter.com/oauth/access_token'


def twitter_login(request):
    # step 1: send req token request to twitter
    resp, content = client.request(request_token_url, "POST")
    if resp['status'] != '200':
        raise Exception("Request token request fail.")

    # step 2: store req token in a session
    print("In Log in :")
    print(request.session.items())
    request_token = request.session['request_token'] = dict(urllib.parse.parse_qsl(content.decode("utf-8")))

    # #step 3: redirect to authentication url
    url = "%s?oauth_token=%s" % (authenticate_url, request.session['request_token']['oauth_token'])
    return HttpResponseRedirect(url)


@login_required(login_url='/socialtracker/')
def twitter_logout(request):
    print(request.session.items())
    twt_logout(request)
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

    # step 3: store user id with screen name
    access_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))
    try:
        user = UserInfo.objects.get(username=access_token['screen_name'])
    except UserInfo.DoNotExist:
        # creat user if not already exist
        user = UserInfo.objects.create_user(access_token['screen_name'], '%s@twitter.com' % access_token['screen_name'],
                                        password=access_token['oauth_token_secret'])
        print("After created")
        print(user)

        profile = TwitterProfile()
        profile.user = user
        profile.t_token = access_token['oauth_token']
        profile.t_secret = access_token['oauth_token_secret']
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

    # return HttpResponseRedirect('/socialtracker/account')
    return HttpResponseRedirect('/%s/account' % app_name)


# The main page.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':  # when submit the form
        uf = RegisterForm(request.POST)  # include the data submitted
        if uf.is_valid():  # if the data submitted is valid
            username = request.POST.get('username', '')
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            password_confirm = request.POST.get('password_confirm', '')
            if password != password_confirm:
                return render(request, 'signup.html', {'uf': uf, 'message': 'please confirm your new password!'})
            else:
                try:
                    UserInfo.objects.create_user(username=username, password=password, email=email,
                                                 phone='0', first_name=first_name, last_name=last_name)
                    return login(request)
                except:
                    return render(request, 'signup.html', {'uf': uf, 'message': 'user has existed！'})
        else:
            return render(request, 'signup.html', {'uf': uf,
                                                   'message': 'Please fill in all information or note the format of '
                                                              'entered password!'})
    else:
        uf = RegisterForm()
        return render(request, 'signup.html', {'uf': uf})


def login(request):
    if request.method == "POST":
        uf = LoginForm(request.POST, instance=profile)
        if uf.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                request.session['username'] = user.username
                request.session['password'] = user.password
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name
                request.session['email'] = user.email
                request.session['phone'] = user.phone
                request.session['city'] = user.city
                request.session['zip_code'] = user.zip_code
                request.session['address'] = user.address
                return render(request, 'account-home.html')
            else:
                return render(request, 'login.html',
                              {'uf': uf, 'message': 'username or password is not correct, please check or signup!'})
        else:
            return render(request, 'login.html', {'uf': uf,
                                                  'message': 'please fill in all the information or note the format of entered password!'})
    else:
        uf = LoginForm()
        return render(request, 'login.html', {'uf': uf})


@login_required(login_url='/socialtracker/')
def account(request):
    return render(request, 'account-home.html')


@login_required(login_url='/socialtracker/')
def manage1(request):
    if request.method == "POST":
        uf = ChangepassForm(request.POST)
        if uf.is_valid():
            username = request.session.get('username')
            old_password = request.POST.get('old_password', '')
            user = auth.authenticate(username=username, password=old_password)
            if user is not None and user.is_active:
                new_password1 = request.POST.get('new_password1', '')
                if new_password1 == old_password:
                    return render(request, 'Manage1_privacy.html',
                                  {'uf': uf, 'message': 'Please set one different new password!'})
                else:
                    new_password2 = request.POST.get('new_password2', '')
                    if new_password1 != new_password2:
                        return render(request, 'Manage1_privacy.html',
                                      {'uf': uf, 'message': 'Please confirm your new password!'})
                    else:
                        user.set_password(new_password1)
                        user.save()
                        return render(request, 'Manage1_privacy.html', {'uf': uf, 'message': 'success!'})
            else:
                return render(request, 'Manage1_privacy.html',
                              {'uf': uf, 'message': 'Your old password is not correct!'})
        else:
            return render(request, 'Manage1_privacy.html', {'uf': uf, 'message':
                'Please fill in all the information or note the format of entered password (at least 8 characters, including both numbers and letters)!'})
    else:
        uf = ChangepassForm()
        return render(request, 'Manage1_privacy.html', {'uf': uf})


@login_required(login_url='/socialtracker/')
def manage2(request):
    if request.method == "POST":
        uf = EdituserinfoForm(request.POST)
        if uf.is_valid():
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            address = request.POST.get('address', '')
            phone = request.POST.get('phone', '')
            zip_code = request.POST.get('zip_code', '')
            gender = request.POST.get('gender', '')
            state = request.POST.get('state', '')
            city = request.POST.get('city', '')
            username = request.session.get('username')
            UserInfo.objects.filter(username=username).update(first_name=first_name, last_name=last_name,
                                                              address=address, phone=phone, zip_code=zip_code,
                                                              gender=gender,
                                                              state=state, city=city)
            user = UserInfo.objects.get(username=username)
            request.session['username'] = user.username
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['phone'] = user.phone
            request.session['city'] = user.city
            request.session['zip_code'] = user.zip_code
            request.session['address'] = user.address
            return render(request, 'Manage2_Personal.html', {'uf': uf, 'message': 'success!'})
        else:
            return render(request, 'Manage2_Personal.html',
                          {'uf': uf, 'message': 'Please fill in all your information!'})
    else:
        uf = EdituserinfoForm()
        return render(request, 'Manage2_Personal.html', {'uf': uf})


@login_required(login_url='/socialtracker/')
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
        facebook_account = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    social_backend = request.session['social_auth_last_login_backend']
    return render(request, 'Manage3_social.html',
                  {'social_backend': social_backend, 'twitter_account': twitter_account, 'twitter_date': twitter_date,
                   'twitter_name': twitter_name, 'facebook_account': facebook_account, 'facebook_date': facebook_date,
                   'facebook_id': facebook_id, 'can_disconnect': can_disconnect})


@login_required(login_url='/socialtracker/')
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})


@login_required(login_url='/socialtracker/')
def data(request):
    user = request.user
    radarData = []
    try:
        twitter_account = user.social_auth.get(provider='twitter')
        if twitter_account is not None:
            twitter_json = twitter_account.extra_data

            # retriev user timeline from twitter
            auth = tweepy.OAuthHandler(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
            auth.set_access_token(twitter_json['access_token']['oauth_token'],
                                  twitter_json['access_token']['oauth_token_secret'])
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

                # format the values data to pipeline for radar chart
                radarObj = []
                for eachNeed in needs:
                    temp = {"axis": "Need " + eachNeed["name"], "value": round(eachNeed["raw_score"], 2),
                            "percentile": round(eachNeed["percentile"], 2)}
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

    return render(request, 'data.html', {'radarData': radarData})


# Enter email address to reset password
class MyPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    form_class = MyPasswordResetForm


# Email Sent
class MyPasswordResetDone(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


# Reset the password without requirement of the old password
class MyPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'


# Password changed and go back to login
class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    ####################################################
    # This two views below are for changing password with requirement of old password.
    ####################################################

    # class MyPasswordChangeView(PasswordChangeView):
    # template_name = 'password_change.html'

    # class MyPasswordChangeDoneView(PasswordChangeDoneView):
    # template_name = 'password_reset_complete.html'


def user_personality(request):
    personality = request.session['user_personality']
    sbData = {'name': 'Sources', 'color': "#d8c51d", 'percent': '', 'children': []}
    totalScore = 0.0
    # top level children list
    for eachPersonality in personality:
        # to hold 5 traits within each personality
        onePersonality = {'name': eachPersonality['name'], 'color': "#d8c51d",
                          'size': round(eachPersonality['raw_score'], 4), 'percent': 0, 'children': []}
        trait1 = eachPersonality['children'][0]
        trait2 = eachPersonality['children'][1]
        trait3 = eachPersonality['children'][2]
        trait4 = eachPersonality['children'][3]
        trait5 = eachPersonality['children'][4]
        totalScore = trait1['raw_score'] + trait2['raw_score'] + trait3['raw_score'] + trait4['raw_score'] + trait5[
            'raw_score']
        child1 = {'name': trait1['name'], 'color': '#d8c51d', 'size': round(trait1['raw_score'], 4),
                  'percentile': round(trait1['percentile'], 4), 'percent': round(trait1['raw_score'] / totalScore, 4)}
        child2 = {'name': trait2['name'], 'color': '#d8c51d', 'size': round(trait2['raw_score'], 4),
                  'percentile': round(trait2['percentile'], 4), 'percent': round(trait2['raw_score'] / totalScore, 4)}
        child3 = {'name': trait3['name'], 'color': '#d8c51d', 'size': round(trait3['raw_score'], 4),
                  'percentile': round(trait3['percentile'], 4), 'percent': round(trait3['raw_score'] / totalScore, 4)}
        child4 = {'name': trait4['name'], 'color': '#d8c51d', 'size': round(trait4['raw_score'], 4),
                  'percentile': round(trait4['percentile'], 4), 'percent': round(trait4['raw_score'] / totalScore, 4)}
        child5 = {'name': trait5['name'], 'color': '#d8c51d', 'size': round(trait5['raw_score'], 4),
                  'percentile': round(trait5['percentile'], 4), 'percent': round(trait5['raw_score'] / totalScore, 4)}
        onePersonality['children'].append(child1)
        onePersonality['children'].append(child2)
        onePersonality['children'].append(child3)
        onePersonality['children'].append(child4)
        onePersonality['children'].append(child5)
        sbData['children'].append(onePersonality)
        totalScore += eachPersonality['raw_score']

    sbData['children'][0]['percent'] = round(personality[0]['raw_score'] / totalScore, 4)
    sbData['children'][1]['percent'] = round(personality[1]['raw_score'] / totalScore, 4)
    sbData['children'][2]['percent'] = round(personality[2]['raw_score'] / totalScore, 4)
    sbData['children'][3]['percent'] = round(personality[3]['raw_score'] / totalScore, 4)
    sbData['children'][4]['percent'] = round(personality[4]['raw_score'] / totalScore, 4)

    return render(request, 'user_personality.html', {'sbData': sbData})


def user_values(request):
    values = request.session['user_values']
    radarObj = []
    for eachValue in values:
        temp = {"axis": eachValue["name"], "value": round(eachValue["raw_score"], 2),
                "percentile": round(eachValue["percentile"], 2)}
        radarObj.append(temp)
    print(radarObj)
    radarData = simplejson.dumps(radarObj)
    return render(request, 'user_values.html', {'radarData': radarData})


# create a dictionary to count user's posts number from Twitter and Facebook.
def tf_count():
    days = list(range(1,8))
    hours = list(range(1,25))
    dic = {}
    for day in days:
        for hour in hours:
            dic[str(day)+str(hour)] = 0
    return dic


def user_post_count(request):
    user = request.user
    tfCount = tf_count()
    # count  number of Tweets
    try:
        twitter_account = user.social_auth.get(provider='twitter')
        if twitter_account is not None:
            twitter_json = twitter_account.extra_data

            # retriev user timeline from twitter
            auth = tweepy.OAuthHandler(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
            auth.set_access_token(twitter_json['access_token']['oauth_token'],
                                  twitter_json['access_token']['oauth_token_secret'])
            api = tweepy.API(auth)
            data = api.user_timeline()


            for each in data:
                created_time = each.created_at
                weekday = created_time.isoweekday()
                hour = created_time.hour
                if hour == 0:
                    hour = 24
                tfCount[str(weekday) + str(hour)] += 1
    except:
        twitter_account = None

    # cont number of Fackbook posts
    try:
        fackbook_account = user.social_auth.get(provider='facebook')
        if fackbook_account is not None:
            fackbook_json = fackbook_account.extra_data
            # temperory fackbook token
            facebook_token = 'EAACEdEose0cBAHH9KlhGpDtH1mvJQrPuhXqlSGZC88FfccdGizFZBZC2ODs9jRul1UJeSW968GLn7ClfM7KhrtXYx2ZBZBcpXZAvujH0F4gTPagF6YVa72gkOMYg0eaT6r6LPEUh49iDKHXUNrwZCZA6UZBpDuzekqNWJK36YKog3LtZB27t6R174ekCGXCR0QJT8xZADO8PGisEgZDZD'
            person = 'https://graph.facebook.com/v3.0/me/posts?access_token=' + facebook_token
            f_posts = requests.get(person).json().get('data')
            for post in f_posts:
                message = post.get('message')
                created_time = post.get('created_time')
                datetime_object = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S+%f')

                if message != None:
                    weekday = datetime_object.isoweekday()
                    hour = datetime_object.hour
                    if hour == 0:
                        hour = 24
                    string = str(weekday) + str(hour)
                    # print('string = ', string)
                    tfCount[string] += 1
    except:
        fackbook_account = None
    request.session['user_postNum'] = tfCount
    return render(request, 'data.html', {'heatmapData': tfCount})


def user_post_num(request):
    post_num = request.session['user_postNum']
    heatmapData = simplejson.dumps(post_num)
    return render(request, 'data.html', {'heatmapData': heatmapData})


