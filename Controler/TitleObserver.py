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
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
                url = url.string
                req = urllib.request.Request(url, None, headers)
                content = urllib.request.urlopen(req)
                print(content)
                titleRE = re.compile("<title>(.+?)</title>")
                title = titleRE.search(content.read().decode('utf8')).group(1)
                print(title)
                Connection.singleton().send_channel(title)
            except Exception as exc:
                print(exc)
                pass
