# COMP90044 Distributed Computing Project
# Web-based mental analytics app on social media
# Author: Xin Wang, Yiwen Zeng, Yu Han, Chenxi Hou
# Created on: 03/2018

# Python Import
import oauth2 as oauth
import urllib.parse

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

"""
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

"""

# The main page.
def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        uf = LoginForm(request.POST)
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
    # social_backend = request.session['social_auth_last_login_backend']
    # return render(request, 'Manage3_social.html', {'social_backend': social_backend})

    user = request.user
    try:
        github_login = user.social_auth.get(provider='github')
        # github_json = github_login.extra_data
        # GithubProfile.g_token = github_json['access_token']
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'Manage3_social.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


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
    return render(request, 'data.html')


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