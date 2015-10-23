# -*- coding: utf-8 -*-
from __future__ import absolute_import
import requests
from requests.exceptions import Timeout, ConnectionError
from uthportal.logger import get_logger

links ={
    'main': 'https://euniversity.uth.gr/unistudent/main.asp?mnuid=mnuMain&',
    'login': 'https://euniversity.uth.gr/unistudent/login.asp?mnuID=student&',
    'grades': 'https://euniversity.uth.gr/unistudent/stud_CResults.asp?studPg=1&mnuid=mnu3&',
    'logout': 'https://euniversity.uth.gr/unistudent/disconnect.asp?mnuid=mnu7&',
    'redirected_url': 'https://euniversity.uth.gr/unistudent/studentMain.asp'
    }

class GradesProvider(object):
    def __init__(self, settings):
        self.logger = get_logger('grades', settings)
        if not self._check_vpn():
            self.logger.error("VPN not connected")
        self._session = requests.Session()
        self._logged_in = False

    def get_grades(self):
        if not self._logged_in:
            self.logger.error('get_grades: Not logged in')
            return False
        try:
            response = self._session.post(links['grades'])
            return response.text
        except ConnectionError:
            self.logger.error('get_grades: Connection error')
            return False
        except Timeout:
            self.logger.error('get_grades: Timeout')
            return False

    def logout(self):
        if not self._logged_in:
            self.logger.warning('Logout: Not logged in')
            return False
        try:
            response = self._session.post(links['logout'])
            if response.status_code == 200:
                return True
        except ConnectionError:
            self.logger.error('LogOut: Connection error')
            return False
        except Timeout:
            self.logger.error('LogOut: Timeout')
            return False

    def login(self, username, password):
        payload = {
            'userName': username,
            'pwd': password,
            'submit1': '%C5%DF%F3%EF%E4%EF%F2',
            'loginTrue': 'login'
        }

        try:
            #get main page to create a cookie
            response = self._session.get(links['main'])
            if response.status_code != 200:
                return False
            #now try to login
            response = self._session.post(
                links['login'],
                verify=False,
                data=payload,
            )
            if response.url == links['redirected_url']:
                self._logged_in = True
                return True
            else:
                self._logged_in = False
                return False

        except ConnectionError:
            self.logger.warning('LogIn: Connection error' )
            self._logged_in = False
            return False
        except Timeout:
            self.logger.warning('LogIn: Timeout')
            self._logged_in = False
            return False


    def _check_vpn(self):
        try:
            r = requests.get(links['main'], timeout=3)
            return r.status_code == 200
        except (Timeout):
            self.logger.debug("Connection timed out. VPN not connected.")
            return False
