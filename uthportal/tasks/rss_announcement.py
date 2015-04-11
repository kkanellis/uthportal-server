#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uthportal.tasks.announcement import AnnouncementTask
from uthportal.util import parse_rss

class RssAnnouncementTask(AnnouncementTask):

    def update(self):
        link = self._get_document_field(self.document, 'link')
        if not link:
            self.logger.error('"link" field is not present')
            return

        new_document_fields = {
            'entries': parse_rss(link)
        }

        # Check any new data exist
        if any( field_data for field_data in new_document_fields.items() ):
            super(AnnouncementTask, self).update(new_fields=new_document_fields)
        else:
            self.logger.warning('No dictionary field contains new data.')

