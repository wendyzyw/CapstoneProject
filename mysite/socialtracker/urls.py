
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	# url('', include('django.contrib.auth.urls', namespace='auth')),
	path('', include('social_django.urls',namespace='social')),
	path('', views.index, name='index'),
	#normal login
	path('login', views.login, name='login'),
	path('signup', views.signup, name='signup'),
	path('forgetPw', views.forgetPw, name='forgetPw'),
	url(r'^twitter_login/?$', views.twitter_login, name="twitter_login"),
	url(r'^twitter_logout/?$', views.twitter_logout, name="twitter_logout"),
	url(r'^twitter_login/authenticated/?$', views.twitter_authenticated, name="twitter_authenticated"),
	
	path('account', views.account, name='account'),
	path('manage1', views.manage1, name='manage1'),
	path('manage2', views.manage2, name='manage2'),
	path('manage3', views.manage3, name='manage3'),
	# try using block template
	path('data', views.data, name='data'),
	path('radarChart', views.radarChart, name='radarChart'),
	# social media login
	path('oauth', include('social_django.urls', namespace='social')), 
]