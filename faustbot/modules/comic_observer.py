import random
import urllib

from comics import *
from faustbot.communication.connection import Connection
from faustbot.modules.comic_scraper import ComicScraper
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class ComicObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return ['.comic']

    @staticmethod
    def help():
        return '.comic liefer einen Link zu einem zufälligen Comic.'

    def update_on_priv_msg(self, data, connection: Connection):
        if data.message.find('.comic') == -1:
            return

        # Join list of comics that have a web based random functionality and those that need a scraper
        all_comics = comics + scraper_comics

        # Choose from the joined list
        comic = random.choice(all_comics)

        # Check which type of comic it is: If it's one that doesn't need a scaper, get the url and return it.
        # If it needs a scraper, use ComicScraper to scrape the comic.
        # If you want to add custom comic scrapers: Look at comic_scraper.py and insert your functionality.
        if comic not in scraper_comics:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
            req = urllib.request.Request(comic, None, headers)
            resource = urllib.request.urlopen(req)
            title = get_title(resource)
            connection.send_back(resource.geturl() + " " + title, data)
        else:
            connection.send_back(ComicScraper.get_random_comic(comic), data)
