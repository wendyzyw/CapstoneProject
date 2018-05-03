from socialtracker.models import Profile, TwitterProfile, FacebookProfile
from django.contrib.auth.models import User

def save_profile(backend, user, response, *args, **kwargs):
	print(backend.provider)
	if type(backend) is 'social_core.backends.facebook.FacebookOauth2':
		fbProfile = FacebookProfile()
		fbProfile.fb_id = response['id']
		fbProfile.fb_email = response['email']
		fbProfile.fb_access_token = response['access_token']
		print(fbProfile.fb_email)
		fbProfile.save()
	# access_token = response['access_token']
	# username = access_token['screen_name']
	# findUser = User.objects.get(username=username)
	
	# profile = Profile()
	# profile.user = findUser
	# profile.oauth_token = access_token['oauth_token']
	# profile.oauth_secret = access_token['oauth_token_secret']
	# profile.social_use_id = response['id']
	# profile.social_usename = username
	# profile.profile_image_url = response['profile_image_url']
	# print(profile.profile_image_url)
	# profile.save()