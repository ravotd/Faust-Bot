from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
import random
import urllib
from FaustBot.Modules.TitleObserver import TitleObserver


class ComicObserver(PrivMsgObserverPrototype):

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.comic') == -1:
            return
        comics = ['https://c.xkcd.com/random/comic/', 'http://www.commitstrip.com/?random=1']
        comic = random.choice(comics)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        req = urllib.request.Request(comic, None, headers)
        resource = urllib.request.urlopen(req)
        title = TitleObserver.getTitle(TitleObserver(), resource)
        connection.send_back(resource.geturl() + " " + title, data)
