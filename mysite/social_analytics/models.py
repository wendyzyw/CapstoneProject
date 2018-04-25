from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
class UserInfo(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    phone = models.IntegerField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, blank=True)

    # is_superuser = models.BooleanField(default=False)

    # objects = MyUserManager
    class Meta:
        db_table = 'UserInfo'

    def __str__(self):
        return self.username  # username and email are primary key, unique


class FackbookProfile(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    facebookToken = models.CharField(max_length=100, blank=True)
    result = models.CharField(max_length=100, blank=True)


class TwitterProfile(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    twitterToken = models.CharField(max_length=100, blank=True)
    result = models.CharField(max_length=100, blank=True)
