from django.contrib import admin

# Register your models here.
#from .models import UserWarning
#admin.site.register(User)
from django.contrib import admin
from social_analytics.models import UserInfo
admin.site.register(UserInfo)