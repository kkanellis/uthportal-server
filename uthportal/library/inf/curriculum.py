#!/usr/bin/python
# -*- coding: utf8 -*-

import os.path

from uthportal.tasks.static import StaticTask

class curriculum(StaticTask):
    filename = 'curriculum.html'
    filedir = os.path.dirname(__file__)

    document_prototype = {
        'type': 'curriculum',
        'entries': [ ]
    }

    def parse(self, bsoup):
        # Find all divs (for all 5 days of the week)
        divs = bsoup.find_all('div', class_='tab_content')

        # days = [ u'Δευτέρα', u'Τρίτη', u'Τετάρτη', u'Πέμπτη', u'Παρασκευή' ]
        cell_key = ['timespan', 'course_name', 'class_type', 'classroom', 'instructor' ]
        curriculum = [ ]
        for (day, cc) in enumerate(divs):
            rows = cc.find_all('tr') # Split to rows
            for row in rows:
                # Contructing entry
                entry = {
                    cell_key[index] : cell.text
                    for index, cell in enumerate(row.find_all('td'))
                }

                # Check if valid entry
                if not entry:
                    continue

                # Special parsing for time (start_time, end_time)
                entry['start_time'], entry['end_time'] = entry['timespan'].split(u'–')
                del entry['timespan']

                # Stripping whitespaces & adding day
                entry = { key: value.strip() for key, value in entry.iteritems() }
                entry['day'] = day

                curriculum.append(entry)

        return curriculum


    def post_process(self):
        """
        Add the 'curriculum' field into 'info' key of every course in entries
        """

        entries = self._get_document_field(self.document, 'entries')

        # Organize entries by course name
        courses_curriculum = { }
        for entry in entries:
            course_name = entry['course_name']
            if course_name in courses_curriculum:
                courses_curriculum[course_name].append(entry)
            else:
                courses_curriculum[course_name] = [ entry ]

        db_manager = self.database_manager
        db_collection = 'inf.courses'

        # Update each course's info
        for (course_name, curriculum) in courses_curriculum.iteritems():
            db_query = { 'info.name': course_name }
            document = db_manager.find_document(db_collection, db_query)


            if not document:
                self.logger.warning('No database entry found for course "%s"' % course_name)
                continue

            if 'curriculum' in document['info']:
                self.logger.debug(
                    'Overwritting previous curriculum: %s'
                    % unicode( self._get_document_field(document, 'info.curriculum'))
                )

            db_manager.update_document(db_collection, db_query, { '$set': { 'info.curriculum' : curriculum } })
            self.logger.debug('Curriculum updated successfully for "%s"' % document['code'])



