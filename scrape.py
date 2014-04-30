import sys
from urllib2 import Request, urlopen, URLError
from urlparse import urlparse
from bs4 import BeautifulSoup
import urllib

WIKI = "Spigot_algorithm"

class Wikipedia:
    locale = 'en'
    host = 'wikipedia.org'

    def __init__(self, wiki_page):
        self.wiki_page = wiki_page

    '''
        Checks if specified url is a Wikipedia page
    '''
    @classmethod
    def is_wiki_link(cls, url, locale='en', exclude_internal=True):
        if url:
            o = urlparse(url)
            if o.path and o.path.startswith('/wiki/'):
                loc = o.hostname.split('.')[0] if o.hostname else locale
                if (exclude_internal and  ":" in o.path) or loc != locale:
                    return None
                return o.path[6:]
        return None

    def _make_request(self, URL):
        req = Request(URL)
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            # everything is fine
            return response

    def to_url(self):
        domain = self.locale + "." + self.host
        url_parts = ["http:/", domain, "wiki", self.wiki_page]
        url = "/".join(url_parts)
        return url

    def request(self):
        domain = self.locale + "." + self.host
        url_parts = ["http:/", domain, "wiki", self.wiki_page]
        url = "/".join(url_parts)
        response = self._make_request(url)
        return self._parse_response(response, self.locale, url)

    def _parse_response(self, response, locale, original_link):
        soup = BeautifulSoup(response)
        wiki_links = set()

        original_wiki = Wikipedia.is_wiki_link(original_link, locale)

        if not original_wiki:
            print "Specified original link is not a Wikipedia page!"
            return "Error parsing page."

        for link in soup.find_all('a'):
            href = link.get('href')
            # A wiki page usually starts with '/wiki/' and shouldn't contain ':' (internal pages)
            # Also need to exclude '/wiki/Main_Page' and original link

            wiki = Wikipedia.is_wiki_link(href, locale)

            if wiki and wiki != original_wiki and wiki != 'Main_Page':
                wiki_links.add(wiki)
        return list(wiki_links)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        WIKI = sys.argv[1]
    links = Wikipedia(WIKI).request()
    links = sorted(links)
    for link in links:
        print urllib.unquote(link.encode('UTF-8'))
    print "Number of Wiki links found: ", len(links)


