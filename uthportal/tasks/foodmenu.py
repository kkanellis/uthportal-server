#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, errno, devnull
from subprocess import call
from datetime import datetime, timedelta

from uthportal.tasks.base import BaseTask
from uthportal.util import download_file

class FoodmenuTask(BaseTask):
    task_type = 'FoodmenuTask'

    update_fields = [ 'menu' ]
    db_query_format = { 'city' : 'id' }

    weekdays = [ 'Δευτέρα', 'Τρίτη', 'Τετάρτη', 'Πέμπτη', 'Παρασκευή', 'Σάββατο', 'Κυριακή' ]

    def __init__(self, path, settings, database_manager, pushd_client):
        super(FoodmenuTask, self).__init__(path, settings, database_manager, pushd_client)

    def update(self):
        # Finding the date of the latest monday
        self.latest_monday = (datetime.now() - timedelta(datetime.now().weekday())).date()

        new_document_fields = {
            'menu': self.__check_menu()
        }

        # Check any new data exist
        if any( field_data for field_data in new_document_fields.items() ):
            super(FoodmenuTask, self).update(new_fields=new_document_fields)
        else:
            self.logger.warning('No dictionary field contains new data.')

    def __check_menu(self):
        link = self._get_document_field(self.document, 'link')
        if not link:
            self.logger.error('"link" not found in document!')
            return None
        else:
            link = link % (self.latest_monday.year, self.latest_monday.month, self.latest_monday.day)

        path_prototype = path.join(self.settings['tmp_path'], unicode(self.latest_monday))
        path_doc = path_prototype + '.doc'
        path_html = path_prototype + '.html'


        success = download_file(link, path_doc)
        if not path.exists(path_doc):
            self.logger.error('Could not write menu_doc to file "%s"' % path_doc)
            return None

        html = self.get_html(path_doc, path_html)
        if not html:
            self.logger.warning('Converted HTML is empty')
            return None

        try:
            foodmenu = self.parse(html)
        except Exception as e:
            self.logger.error('parse: %s' % e)
            return None

        return foodmenu

    def get_html(self, path_doc, path_html):
        """
        Uses soffice library ( used by LibreOffice & OpenOffice ) to convert
        the .doc file to the according .html one.

        Reference:
        https://help.libreoffice.org/Common/Starting_the_Software_With_Parameters
        """

        # Write the .doc menu to a file
        # set the arguments and make the call
        soffice_args = ['soffice', '--headless', '--convert-to', 'html:HTML', '--outdir', self.settings['tmp_path'], path_doc ]

        # Open stream to write to /dev/null
        with open(devnull, 'w') as DEV_NULL:
            try:
                ret_code = call(soffice_args, stdout=DEV_NULL)
            except OSError as e:
                if e.errno == errno.ENOENT:
                    self.logger.error("soffice not found!")
                else:
                    self.logger.error('soffice: %s' % str(e))

                return None

        if ret_code != 0 or (not path.exists(path_html)):
            self.logger.error('Could not convert .doc to .html')
            return None

        # Read the html produced
        with open(path_html, 'rb') as f:
            html = f.read()

        if not html:
            self.logger.error('File "%s" is empty' % path_html)
            return None

        return html

    def prettify(self, text):
        """
        Strips the starting and trailing whitespaces from text as well
        as the unecessary -multiple- whitspaces found between the words
        due to bad formating

        Also remove any unecessary informations.
        """
        special_menu = u'ΕΙΔΙΚΟ ΜΕΝΟΥ'

        pretty_text = u''
        is_whitespace = False
        for i in xrange(len(text)):
            if text[i].isspace() and not is_whitespace:
                # first whitespace character found after a non-whitespace one
                pretty_text += ' '
                is_whitespace = True
            elif not text[i].isspace():
                # normal character
                pretty_text += text[i]
                is_whitespace = False

        # removes the 'special_menu' string from the text
        new_end = pretty_text.find(special_menu)
        if new_end is not -1:
            pretty_text = pretty_text[:new_end]

        return pretty_text
