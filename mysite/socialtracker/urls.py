from django.urls import path, include

from . import views

urlpatterns = [
    # social media login
    path('', include('social_django.urls', namespace='social')),
    # main page
    path('', views.index, name='index'),
    # normal login
    path('login', views.login, name='login'),
    path('account', views.account, name='account'),
    path('manage1', views.manage1, name='manage1'),
    path('manage2', views.manage2, name='manage2'),  # change password
    path('manage3', views.manage3, name='manage3'),  # social account management
    path('manage3/password/', views.password, name='password'),  # add password if log in from social media
    path('signup', views.register, name='signup'),
    # url(r'^twitter_logout/?$', views.twitter_logout, name="twitter_logout"),
    path('twitter_logout/', views.twitter_logout, name="twitter_logout"),
    # try using block template
    path('data', views.data, name='data'),
    # reset password, say, send email
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

    # data visualiazation
    path('user_values', views.user_values, name='user_values'),
    path('user_personality', views.user_personality, name='user_personality'),
    path('tone_analysis', views.tone_analysis, name='tone_analysis'),
    path('keywords', views.keywords, name='keywords'),
    path('social_network', views.social_network, name='social_network'),
    path('time_heatmap', views.time_heatmap, name='time_heatmap'),
    path('bubble',views.get_hashtag_list, name='bubble'),

]
