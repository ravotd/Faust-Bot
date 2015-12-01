import re
import urllib

from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class TitleObserver(PrivMsgObserverPrototype):

    def update_on_priv_msg(self, data):
        url = re.search("(?P<url>https?://[^\s]+)", data['message'])
        if url is not None:
            try:
                url = url.string
                content = urllib.request.urlopen(url)
                titleRE = re.compile("<title>(.+?)</title>")
                title = titleRE.search(content.read().decode('utf8')).group(1)
                Connection.singleton().send_channel(title)
            except Exception as exc:
                pass