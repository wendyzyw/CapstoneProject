from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.login, name='login'),
	# path('dataview', views.dataview, name='dataview'),
	path('account', views.account, name='account'),
	path('manage1', views.manage1, name='manage1'),
	path('manage2', views.manage2, name='manage2'),
	path('manage3', views.manage3, name='manage3'),
	# try using block template
	path('data', views.data, name='data'),
]