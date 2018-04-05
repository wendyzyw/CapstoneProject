
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from social_analytics.views import twitter_login, twitter_logout, twitter_authenticated

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	#normal login
	path('login', views.login, name='login'),
	#social media login
	url(r'^login/?$', twitter_login),
    url(r'^logout/?$', twitter_logout),
    url(r'^login/authenticated/?$', twitter_authenticated),
	
	path('account', views.account, name='account'),
	path('manage1', views.manage1, name='manage1'),
	path('manage2', views.manage2, name='manage2'),
	path('manage3', views.manage3, name='manage3'),
	# try using block template
	path('data', views.data, name='data'),
	# social media login
	path('oauth', include('social_django.urls', namespace='social')), 
]