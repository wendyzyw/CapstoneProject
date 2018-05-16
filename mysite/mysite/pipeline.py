from social_core.backends.facebook import FacebookOAuth2
from social_core.backends.google import GoogleOAuth2
from social_core.backends.linkedin import LinkedinOAuth
from social_core.backends.twitter import TwitterOAuth
import sys
sys.path.append('../')
from socialtracker.models import UserInfo


def update_user_social_data(strategy, *args, **kwargs):
    """Set the name and avatar for a user only if is new.
    """
    print ('update_user_social_data ::', strategy)
    if not kwargs['is_new']:
        return

    full_name = ''
    email = ''
    backend = kwargs['backend']

    user = kwargs['user']

    # set user's email
    if (
        isinstance(backend, GoogleOAuth2)
        or isinstance(backend, FacebookOAuth2)
    ):
        full_name = kwargs['response'].get('name')
        email = kwargs['response'].get('email')
    elif (
        isinstance(backend, LinkedinOAuth)
        or isinstance(backend, TwitterOAuth)
    ):
        print('twitter login')
        if kwargs.get('details'):
            full_name = kwargs['details'].get('fullname')
            print('full_name = ', full_name)
            email = kwargs['response'].get('email')
            print('email = ', email)

    user.full_name = full_name
    UserInfo.email = email
    UserInfo.save()
    print('email = ', UserInfo.email)

    user.save()

    # set user's image
    """
    if isinstance(backend, GoogleOAuth2):
        if response.get('image') and response['image'].get('url'):
            url = response['image'].get('url')
            ext = url.split('.')[-1]
            user.avatar.save(
               '{0}.{1}'.format('avatar', ext),
               ContentFile(urllib2.urlopen(url).read()),
               save=False
            )
    elif isinstance(backend, FacebookOAuth2):
        fbuid = kwargs['response']['id']
        image_name = 'fb_avatar_%s.jpg' % fbuid
        image_url = 'http://graph.facebook.com/%s/picture?type=large' % fbuid
        image_stream = urlopen(image_url)

        user.avatar.save(
            image_name,
            ContentFile(image_stream.read()),
        )
       

    if isinstance(backend, TwitterOAuth):
        if kwargs['response'].get('profile_image_url'):
            image_name = 'tw_avatar_%s.jpg' % full_name
            image_url = kwargs['response'].get['profile_image_url']
            image_stream = request.urlopen(image_url)

            user.avatar.save(
                image_name,
                ContentFile(image_stream.read()),
            )
    # LinkedinOAuth
    
    elif isinstance(backend, LinkedinOAuth):
        if kwargs['response'].get('pictureUrl'):
            image_name = 'linked_avatar_%s.jpg' % full_name
            image_url = kwargs['response'].get['pictureUrl']
            image_stream = urlopen(image_url)

            user.avatar.save(
                image_name,
                ContentFile(image_stream.read()),
            )
    
    user.save()
    """