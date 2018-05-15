"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qmp0zuh2g%4o)gyr3x#y3*qyl8anpqb80b!%kdy%f8+p9zusiv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['lorikeetanalysis.net','localhost']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
	'socialtracker.apps.SocialAnalyticsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	# 'socialtracker',
	'social_django',
	'rest_framework.authtoken'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'social_django.middleware.SocialAuthExceptionMiddleware', #social auth
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
				'social_django.context_processors.backends',  # social auth
                'social_django.context_processors.login_redirect', # social auth
            ],
        },
    },
]

SOCIAL_AUTH_PIPELINE = (
	'social_core.pipeline.social_auth.social_details',
	'social_core.pipeline.social_auth.social_uid',
	'social_core.pipeline.social_auth.social_user',
	'social_core.pipeline.user.get_username',
	# 'social_core.pipeline.user.create_user',
	'mysite.pipeline.create_new_user',
	'social_core.pipeline.social_auth.associate_user',
	'social_core.pipeline.social_auth.load_extra_data',
	'social_core.pipeline.user.user_details',
	'social_core.pipeline.social_auth.associate_by_email',
)

# add extra var to communicate between session (in views) and pipeline 
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['is_associated',]

WSGI_APPLICATION = 'mysite.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#in case of a custome namespace 
SOCIAL_AUTH_URL_NAMESPACE = 'social'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',
	'django.contrib.auth.backends.ModelBackend',
	#Google
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
	#Twitter
    'social_core.backends.twitter.TwitterOAuth',
	#Facebook
	'social_core.backends.facebook.FacebookOAuth2',
	#Reddit
	'social_core.backends.reddit.RedditOAuth2',
	#Tumblr
	'social_core.backends.tumblr.TumblrOAuth',
)

# social keys and tokens
# SOCIAL_AUTH_TWITTER_KEY = 'owCSHnblBoITQhCRZjNFqEuXd'
# SOCIAL_AUTH_TWITTER_SECRET = 'djD1JSM0ZZnSINxpLzTrXKlSAPvvCGd7UEy2pvfFcD2d4nV4R0'
TWITTER_TOKEN = 'AZU8kwktk3IHLdOPjhgZqtiOk'
TWITTER_SECRET = '2ihJ6ZrKBl3p0QGADi4Dx3WRf9OZx5IftZZiFFfMmfkUtev6QY'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = "https://lorikeetanalysis.net/socialtracker/account"
SOCIAL_AUTH_TWITTER_KEY = 'AZU8kwktk3IHLdOPjhgZqtiOk'
SOCIAL_AUTH_TWITTER_SECRET = '2ihJ6ZrKBl3p0QGADi4Dx3WRf9OZx5IftZZiFFfMmfkUtev6QY'
SOCIAL_AUTH_FACEBOOK_KEY = '213217539436188'
SOCIAL_AUTH_FACEBOOK_SECRET = '2f5d61e15d85dc58319c54b0e08aaeb0'
SOCIAL_AUTH_FACEBOOK_APP_NAMESPACE = 'socialtracker'
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.12'
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_EXTENDED_PERMISSIONS = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
	'locale': 'ru_RU',
	'fields': 'id, name, email, age_range'
}
# SOCIAL_AUTH_FACEBOOK_SCOPE = [
	# 'email'
# ]

SOCIAL_AUTH_TUMBLR_KEY = 'IZS8jZq3HRoODrqIIGryRrr78Ry58qavS4j3byCcEWeGkdCS9I'
SOCIAL_AUTH_TUMBLR_SECRET = 'gjbfotuFl54PCaOjEZeVWLDfJy2Z4B4DQ215FKm22KFaDKVaNP'

AUTH_PROFILE_MODULE = 'socialtracker.Profile'


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static')
# 设置图片等静态文件的路径
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)