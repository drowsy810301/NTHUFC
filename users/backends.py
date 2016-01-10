from django.contrib.auth.models import User
from users.models import Account
'''custom authentication resolve 'last_login' problem'''
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
user_logged_in.disconnect(update_last_login)
class EmailAuthBackend(object):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """

    def authenticate(self, username=None, email=None, ID_card=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = Account.objects.get(username=username, email=email, ID_card=ID_card)
            return user
        except Account.DoesNotExist:
            return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return Account.objects.get(pk=user_id)
        except Account.DoesNotExist:
            return None
