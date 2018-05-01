from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserInfo(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    phone = models.IntegerField(blank=True, null=True)
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

    def DoNotExist(self):
        pass


class FackbookProfile(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    f_token = models.CharField(max_length=100, blank=True, null=True)
    f_secret = models.CharField(max_length=100, blank=True, null=True)
    f_profile_image_url = models.URLField(max_length=100, blank=True, null=True)
    f_user_id = models.CharField(max_length=100, blank=True, null=True)
    f_email = models.CharField(max_length=100, blank=True, null=True)
    f_usename = models.CharField(max_length=100, blank=True, null=True)
    f_result = models.CharField(max_length=100, blank=True)


class TwitterProfile(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    t_token = models.CharField(max_length=100, blank=True, null=True)
    t_secret = models.CharField(max_length=100, blank=True, null=True)
    t_profile_image_url = models.URLField(max_length=100, blank=True, null=True)
    t_user_id = models.CharField(max_length=100, blank=True, null=True)
    t_email = models.CharField(max_length=100, blank=True, null=True)
    t_usename = models.CharField(max_length=100, blank=True, null=True)
    t_result = models.CharField(max_length=100, blank=True)
