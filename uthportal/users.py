import uuid
from abc import ABCMeta

import sendgrid

from logger import get_logger
from util import get_first_n_digits, is_equal

def generate_auth_pair() :
   """
   Generates a (user id, activation token) pair
   """
   userid = uuid.uuid4()
   return (get_first_n_digits(userid.int, 8), str(userid))

class UserManager(object):
    def __init__(self, settings, db_manager):
        self.db_manager = db_manager
        self.settings = settings
        self.logger = get_logger('user-control', settings)
        self.users = Users(settings, db_manager)

    def is_auth_id_available(self, auth_id):
        active_user = self.db_manager.find_document(
            'users.active',
            {'auth_id': auth_id}
        )
        pending_user = self.db_manager.find_document(
            'users.pending',
            {'auth_id': auth_id}
        )
        return not (active_user or pending_user)

    def is_token_available(self, token):
        user = self.db_manager.find_document('users.pending', {'token': token})
        return True if not user else False

    def is_activation_pair_available(self, auth_id, token):
        return self.is_token_available(token) and \
            self.is_auth_id_available(auth_id)

    def generate_unique_pair(self):
        (auth_id, token) = generate_auth_pair()
        while not self.is_activation_pair_available(auth_id, token):
            (auth_id, token) = generate_auth_pair()
        return (auth_id, token)

    def register_new_user(self, email):
        """
        Registers a new user.
         >Returns the status response from sendgrid if the registration was
         >successful, None otherwise
        """
        if email in self.users.pending or email in self.users.active:
            #already registered or active user
            return None

        (auth_id, token) = self.generate_unique_pair()
        user_info = {
            'email': email,
            'token': token,
            'auth_id': auth_id,
            'tries': 0
        }
        result = self.users.pending.append(user_info)
        if result:
            pending_user = self.users.pending[email]
            return pending_user.send_activation_mail()
        else:
            return None

################################################################################
# COLLECTIONS
################################################################################
class Users(object):
    """
    Place holder class, to force dot-notaion
    """
    #TODO: is there a better way?
    def __init__(self, settings, db_manager):
        self.active = ActiveUsers(settings, db_manager)
        self.pending = PendingUsers(settings, db_manager)

class BaseUserCollection(object):
    __metaclass__ = ABCMeta
    def __init__(self, settings, db_manager):
        self.db_manager = db_manager
        self.settings = settings

    def __getitem__(self, email):
        """
        Search for a user
        """
        user_info = self.db_manager.find_document(self._collection, {'email': email})
        if not user_info:
            raise KeyError('User not found')

        return self._children_class(self.settings, self.db_manager, user_info)

        #    return ActiveUser(self.settings, self.db_manager, user_info)
        #else:
        #    return PendingUser(self.settings, self.db_manager, user_info)

    def __delitem__(self, email):
        result = self.db_manager.remove_document(self._collection, {'email': email})
        if not result:
            raise KeyError('User not found')

    def __setiitem__(self, email, user):
        #TODO: this is supposed to edit the user
        if not isinstance(user, self._children_class):
            raise KeyError('Invalid user type')
        self.db_manager.insert_document(self._collection, user.info)

    def __contains__(self, email):
        user = self.db_manager.find_document(self._collection, {'email': email})
        return True if user else False

    def append(self, user_info):
        return self.db_manager.insert_document(self._collection, user_info)

class ActiveUsers(BaseUserCollection):
    def __init__(self, settings, db_manager):
        super(ActiveUsers, self).__init__(settings, db_manager)
        self._collection = 'users.active'
        self._children_class = ActiveUser


class PendingUsers(BaseUserCollection):
    def __init__(self, settings, db_manager):
        super(PendingUsers, self).__init__(settings, db_manager)
        self._collection = 'users.pending'
        self._children_class = PendingUser


################################################################################

################################################################################
# CHILDREN
################################################################################

class BaseUser(object):
    __metaclass__ = ABCMeta
    def __init__(self, settings, db_manager, info):
        self.settings = settings
        self.db_manager = db_manager
        self.info = info

class PendingUser(BaseUser):
    def __init__(self, settings, db_manager, info):
        super(PendingUser, self).__init__(settings, db_manager, info)
        self.is_pending = True #TODO:needed?

        for key in ('token', 'tries', 'auth_id', 'email'):
            if key not in info:
                raise ValueError('[%s] not found in info' % key)

        #email settings
        email_settings = self.settings['auth']['email']
        username = email_settings['username']
        password = email_settings['password']

        self._sg = sendgrid.SendGridClient(username, password)
        self._email_from = settings['email']['from']
        self._domain = settings['server']['domain']

    def activate(self, token):
        if is_equal(token, self.info['token']):
            #valid activation, retrieve and remove document
            user = self.db_manager.find_document('users.pending', {'email': self.info['email']})
            self.db_manager.remove_document('users.pending', {'email': self.info['email']})
            #delete unwanted fields
            del user['tries'], user['token']
            return self.db_manager.insert_document('users.active', user)
        else:
            return False

    def send_activation_mail(self):
        message = sendgrid.Mail()
        message.add_to(self.info['email'])
        message.set_subject('UthPortal activation')
        address = self.info['email']
        token = self.info['token']
        auth_id = self.info['auth_id']
        #TODO: make some proper html
        message.set_html(
            "Please click on the following link to activate your account:\
            <a href={0}/api/v1/activate?email={1}&token={2}>Activate</a>, \
            This is your 8-digit unique user id: {3}\
            Use this in your app, when asked for it.\
            This id is used to personalize your push notifications.\
            Please don't share this ID as it is supposed to be kept secret."\
            .format(self._domain, address, token, auth_id))
        message.set_text('Token: {0}, 8-digit: {1}'.format(token, auth_id))
        message.set_from('UthPortal <%s>' % self._email_from)
        return self._sg.send(message)

class ActiveUser(BaseUser):
    def __init__(self, settings, db_manager, info):
        super(ActiveUser, self).__init__(settings, db_manager, info)

        for key in ('auth_id', 'email'):
                if key not in info:
                    raise ValueError('%s not found in arguments' % key)
        self.is_pending = False

    def authenticate(self, auth_id):
        return is_equal(self.info['auth_id'], auth_id)
