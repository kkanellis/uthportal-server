
import requests
from requests.exceptions import ConnectionError, Timeout

class InfSite(object):
    """
    Authentication class for inf-site.
    """

    link = 'https://www.inf.uth.gr/wp-login.php?redirect_to=index.php&lang=el'

    def __init__(self, logger, settings):
        """ Necessary args are: username & password """

        self.logger = logger

        if ('username' in settings and
            'password' in settings):
                self.username, self.password = settings['username'], settings['password']
        else:
            self.logger.error('Username and/or password is missing. Cannot proceed with authentication')

        self.logger.debug('Authenication class initialized successfully!')

    def auth(self, session):
        """ Perform the authentication """

        redirected_url = 'http://www.inf.uth.gr/'
        payload = {
            'log': self.username,
            'pwd': self.password
        }

        self.logger.debug('Perfoming auth @ "%s"... ' % self.link)
        try:
            response = session.post(self.link, verify=False, data=payload)
        except ConnectionError:
            self.logger.warning('%s: Connection error' % self.link)
            return None
        except Timeout:
            self.logger.warning('%s: Timeout' % (self.link))
            return None

        self.success = True if response.url == redirected_url else False


auth_classes = {
    'inf-site' : InfSite
}

