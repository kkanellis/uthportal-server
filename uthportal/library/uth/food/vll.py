#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from uthportal.tasks.foodmenu import FoodmenuTask
from uthportal.util import get_soup, date_to_datetime

class vll(FoodmenuTask):
    document_prototype = {
        'city': 'vll',
        'link': 'http://uth.gr/static/miscdocs/merimna/menusitisis_Χ_%d%02d%02d.doc'
    }

    def parse(self, html):
        """
        Feel free to propose any changes on the schema below.

        Dictionary format:

        'lunch'-> 'main'   -> unicode
                  'salad'  -> unicode
                  'desert' -> unicode

        'dinner'-> 'main'   -> unicode
                   'salad'  -> unicode
                   'desert' -> unicode
        """

        # get the cells from the html
        bsoup = get_soup(html)
        cells = [ self.prettify(cell.text) for cell in bsoup.find_all('td') ]

        # split the cells according to meal. hardcoded positions
        lunch  = [ cells[ 9:16], cells[17:24], cells[25:32] ]
        dinner = [ cells[41:48], cells[49:56], cells[57:64] ]

        # create the menu dictionary
        menu = list()
        for i in xrange(7):
            day_menu = {
                    'name': self.weekdays[i],
                    'date': date_to_datetime(self.latest_monday + timedelta(days=i)),
                    'lunch': {
                        'main': lunch[0][i],
                        'salad': lunch[1][i],
                        'desert': lunch[2][i]
                    },
                    'dinner': {
                        'main': dinner[0][i],
                        'salad': dinner[1][i],
                        'desert': dinner[2][i]
                    }
            }

            menu.append(day_menu)

        return menu

