import uuid

import sendgrid

from logger import get_logger
from util import get_first_n_digits


class UserControl(object):
    def __init__(self, settings, db_manager):
        self.db_manager = db_manager
        self.settings = settings
        self.logger = get_logger('user-control', settings)

        email_settings = self.settings['auth']['email']
        username = email_settings['username']
        password = email_settings['password']

        self._email_from = settings['email']['from']
        self._domain = settings['server']['domain']

        self._sg = sendgrid.SendGridClient(username, password)

    def uuid_exists(self, userid=None, token=None):
        short_query =  { 'uuid' : userid }
        token_exists = None
        if token:
            #Check for activation token
            token_exists = self.db_manager.find_document('users.pending', query = { 'token' : token}) != None
            if not userid:
                return token_exists

        return ( (self.db_manager.find_document('users.pending', query = short_query) is not None) or
                (self.db_manager.find_document('users.active', query = short_query) is not None)  or token_exists)

    @staticmethod
    def generate_uuid() :
       """
       Generates a user id, actiavtion id pair
       and checks for uniqueness in the database
       """
       userid = uuid.uuid4()
       return (get_first_n_digits(userid.int, 8), str(userid))

    def send_activation_email(self, address, userid, token):
        message = sendgrid.Mail()
        message.add_to(address)
        message.set_subject('Test')
        #TODO: make some proper html
        message.set_html(
            "Please click on the following link to activate your account:\
            <a href={0}/api/v1/activate?email={1}&token={2}>Activate</a>, \
            This is your 8-digit unique user id: {3}\
            Use this in your app, when asked for it.\
            This id is used to personalize your push notifications.\
            Please don't share this ID as it is supposed to be kept secret."\
            .format(self._domain, address, token, userid))
        message.set_text('Token: {0}, 8-digit: {1}'.format(token, userid))
        message.set_from('UthPortal <%s>' % self._email_from)
        return self._sg.send(message)

    def generate_and_check(self):
        (userid, token) = self.generate_uuid()
        while self.uuid_exists(userid, token):
            (userid, token) = self.generate_uuid()

        return (userid, token)
