import html
import re
import urllib
from urllib import request

from faustbot.communication.connection import Connection
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype
from faustbot.util import logging


class TitleObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_priv_msg(self, data, connection: Connection):
        regex = "(?P<url>https?://[^\s]+)"
        url = re.search(regex, data.message)
        if url is not None:
            logger = logging.get_logger(self.__name__)
            url = url.group()
            logger.debug('found url: %s', url)
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)', 'Accept-Language': 'de'}
                url = url
                req = urllib.request.Request(url, None, headers)
                resource = urllib.request.urlopen(req)
                title = TitleObserver.get_title(resource)
                logger.debug('fetched title for %s: %s', url, title)
                title = title[:350]
                connection.send_back(title, data)
            except Exception as exc:
                logger.exception(exc)
                pass

    @staticmethod
    def get_title(resource):
        encoding = resource.headers.get_content_charset()
        # der erste Fall kann raus, wenn ein anderer Channel benutzt wird
        if resource.geturl().find('rehakids.de') != -1:
            encoding = 'windows-1252'
        if not encoding:
            encoding = 'utf-8'
        content = resource.read().decode(encoding, errors='replace')
        title_re = re.compile("<title>(.+?)</title>")
        title = title_re.search(content).group(1)
        title = html.unescape(title)
        title = title.replace('\n', ' ').replace('\r', '')
        title = title.replace("&lt;", "<")
        title = title.replace("&gt;", ">")
        title = title.replace("&amp;", "&")
        return title
