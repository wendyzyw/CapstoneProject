from socialtracker.models import Profile
from django.contrib.auth.models import User

USER_FIELDS = ['username', 'email']

def create_new_user(strategy, details, backend, user=None, *args, **kwargs):
	print(backend)
	print(strategy)
	print(args)

	if user:
		return {'is_new': False}

	fields = dict((name, kwargs.get(name, details.get(name)))
				for name in backend.setting('USER_FIELDS', USER_FIELDS))
	if not fields:
		return

	return {
		'is_new': True,
		'user': strategy.create_user(**fields)
	}
