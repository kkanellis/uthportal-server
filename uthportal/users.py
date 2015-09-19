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
        self._email_from = email_settings['from']

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
        message.set_html('Token: {0}, 8-digit: {1}'.format(token, userid))
        message.set_text('Token: {0}, 8-digit: {1}'.format(token, userid))
        message.set_from('UthPortal <%s>' % self._email_from)
        return (205,"a") #self._sg.send(message)

    def generate_and_check(self):
        (userid, token) = self.generate_uuid()
        while self.uuid_exists(userid, token):
            (userid, token) = self.generate_uuid()

        return (userid, token)

