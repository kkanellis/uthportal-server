#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from uthportal.tasks.base import BaseTask

class FoodmenuTask(BaseTask):
    def __init__(self, database_manager):
        super(FoodmenuTask, self).__init__(database_manager)

        self.update_fields = [ 'menu' ]
        self.db_query = { 'city' : self.id }

        self.logger.debug('Loading document from database...')

        self.document = self.load()
        if not self.document:
            if hasattr(self, 'document_prototype'):
                self.logger.info('No document found in database. Using prototype')
                self.document = self.document_prototype
                self.save()
            else:
                self.logger.error('No document_prototype is available!')
                return

        self.logger.debug('id = {:<10} | collection = {:<35}'.format(self.id, self.db_collection))

    def update(self):
        # Finding the date of the latest monday
        self.latest_monday = (datetime.now() - timedelta(datetime.now().weekday())).date()

        new_document_fields = {
                'menu': self.__check_menu()
        }

        # Check any new data exist
        if any( field_data for field_data in new_document_fields.items() ):
            super(CourseTask, self).update(new_fields=new_document_fields)
        else:
            self.logger.warning('No dictionary field contains new data.')

    def __check_menu(self):
        link = _get_document_field(self.document, 'link')
        if not link:
            self.logger.error('"link" not found in document!')
            return None
        else:
            link = link % (self.latest_monday.year, self.latest_monday.month, self.latest_monday.day)

        menu_doc = self.fetch(link)
        if not menu_doc:
            self.logger.warning('Fetch "%s" returned nothing' % link)
            return None

        html = self.convert_to_html(menu_doc)
        if not html:
            self.logger.warning('Converted HTML is empty')
            return None

        try:
            foodmenu = self.parse(html)
        except Exception, e:
            self.logger.error('parse: %s' % e)
            return None

        return foodmenu


    def convert_to_html(menu_doc):
        """
        Uses soffice library ( used by LibreOffice & OpenOffice ) to convert
        the .doc file to the according .html one.

        Reference:
        https://help.libreoffice.org/Common/Starting_the_Software_With_Parameters
        """
        # Write the .doc menu to a file
        path_prototype = path.join(self.settings['tmp_path'], unicode(self.latest_monday))
        path_doc = path_prototype + '.doc'
        path_html = path_prototype + '.html'

        with open(path_doc, 'rw') as f:
            f.write(menu_doc)

        if not path.exists(path_doc):
            self.logger.error('Could not write menu_doc to file "%s"' % path_doc)
            return None

        # set the arguments and make the call
        soffice_args = ['soffice', '--headless', '--convert-to', 'html:HTML', '--outdir', dir_name, doc_path ]
        ret_code = call(soffice_args)

        if ret_code != 0 or not path.exists(path_html):
            self.logger.error('Could not convert .doc to .html')
            return None

        # Read the html produced
        with open(path_html, 'r') as f:
            html = f.read()

        if not html:
            self.logger.error('File "%s" is empty' % path_html)
            return None

        return html

    def prettify(text):
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


