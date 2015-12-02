import re
import urllib
from urllib import request

from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class TitleObserver(PrivMsgObserverPrototype):

    def update_on_priv_msg(self, data):
        url = re.search("(?P<url>https?://[^\s]+)", data['message'])
        if url is not None:
            print(url)
            try:
                url = url.string
                print(url)
                content = urllib.request.urlopen(url)
                print(content)
                titleRE = re.compile("<title>(.+?)</title>")
                title = titleRE.search(content.read().decode('utf8')).group(1)
                print(title)
                Connection.singleton().send_channel(title)
            except Exception as exc:
                print(exc)
                pass
