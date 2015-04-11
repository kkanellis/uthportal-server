from uthportal.tasks.announcement import AnnouncementTask
from uthportal.util import parse_greek_date, get_soup

class general(AnnouncementTask):

    document_prototype = {
        'type': 'general',
        'link': 'http://www.inf.uth.gr/cced/?cat=24',
    }

    def parse(self, bsoup):
        announcements = []

        # get post containining announcements
        posts = bsoup.find(id='post')

        # get articles from post
        articles =  posts.find_all('article', class_='loop-entry clearfix')

        #loop thorugh articles
        for article in articles:
            #initialize announcement dictionary
            announcement = {}

            # get left part
            left = article.find('div', class_='loop-entry-left')
            date_post = left.find('div', class_= 'post-meta').find('div', class_ = 'post-date')
            announcement['date'] = parse_greek_date( date_post.text )

            #get right part
            right = article.find('div', class_='loop-entry-right')

            announcement['title'] = right.h2.a['title']
            announcement['link'] = right.h2.a['href']

            paragraphs = right.find_all( 'p' )

            #join all paragraps to a single html
            announcement['html'] = '\n'.join( [unicode(p) for p in paragraphs] )

            # get the plaintext from html
            bsoup = get_soup(announcement['html'])
            announcement['plaintext'] = bsoup.text.strip()

            #add to announcements
            announcements.append(announcement)


        return announcements

