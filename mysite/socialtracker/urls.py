from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # url('', include('django.contrib.auth.urls', namespace='auth')),
    path('', include('social_django.urls', namespace='social')),
    path('', views.index, name='index'),
    # normal login
    path('login', views.login, name='login'),
    path('signup', views.register, name='signup'),
    path('forgetPw', views.forgetPw, name='forgetPw'),
    # url(r'^twitter_login/?$', views.twitter_login, name="twitter_login"),
    url(r'^twitter_logout/?$', views.twitter_logout, name="twitter_logout"),
    # url(r'^twitter_login/authenticated/?$', views.twitter_authenticated, name="twitter_authenticated"),

    path('account', views.account, name='account'),
    path('manage1', views.manage1, name='manage1'),
    path('manage2', views.manage2, name='manage2'),
    path('manage3', views.manage3, name='manage3'),
    # try using block template
    path('data', views.data, name='data'),
    path('user_values', views.user_values, name='user_values'),
    path('user_personality', views.user_personality, name='user_personality'),
    path('user_preferences', views.user_preferences, name='user_preferences'),
    path('tone_analysis', views.tone_analysis, name='tone_analysis'),
    path('keywords', views.keywords, name='keywords'),
    path('social_network', views.social_network, name='social_network'),
    path('time_heatmap', views.time_heatmap, name='time_heatmap'),
    path('bubble', views.get_hashtag_list, name='bubble'),
    # forget password
    path('password_reset/',
         views.MyPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         views.MyPasswordResetDone.as_view(),
         name='password_reset_done'),
    # change password
    path('password_change/',
         views.PasswordChangeView.as_view(),
         name='change_password'),
    path('password_change/done/',
         views.PasswordChangeDoneView.as_view(),
         name='change_password_done'),
    # confirm password reset
    path('reset/<uidb64>/<token>/',
         views.MyPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         views.MyPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
