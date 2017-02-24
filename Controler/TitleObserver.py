import html
import re
import urllib
from urllib import request

from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class TitleObserver(PrivMsgObserverPrototype):
    def update_on_priv_msg(self, data):
        regex = "(?P<url>https?://[^\s]+)"
        url = re.search(regex, data['message'])
        if url is not None:
            url = url.group()
            print(url)
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
                url = url
                req = urllib.request.Request(url, None, headers)
                resource = urllib.request.urlopen(req)
                encoding = resource.headers.get_content_charset()
                # der erste Fall kann raus, wenn ein anderer Channel benutzt wird
                if url.find('rehakids.de') != -1:
                    encoding = 'windows-1252'
                if not encoding:
                    encoding = 'utf-8'
                content = resource.read().decode(encoding, errors='replace')
                title_re = re.compile("<title>(.+?)</title>")
                title = title_re.search(content).group(1)
                title = html.unescape(title)
                title = title.replace('\n', ' ').replace('\r', '')
                print(title)
                Connection.singleton().send_back(title, data)
            except Exception as exc:
                print(exc)
                pass
