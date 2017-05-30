from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype
import re
import urllib
from urllib import request
import html

class ICDObserver(PrivMsgObserverPrototype):

    def get_icd(self, code):
        url = 'http://www.icd-code.de/icd/code/' + code + '.html'
        print(url)
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
            req = urllib.request.Request(url, None, headers)
            resource = urllib.request.urlopen(req)
            encoding = 'iso-8859-1'
            content =  resource.read().decode(encoding, errors='replace')
            titleRE = re.compile('<title>ICD-10-GM-2017 \s(.+?)\s- ICD10\s</title>')
            title = titleRE.search(content).group(1)
            title = html.unescape(title)
            title = title.replace('\n', ' ').replace('\r', '')
            return title
        except Exception as exc:
            print(exc)
            return 0

    def update_on_priv_msg(self, data):
        regex = "(?P<url>https?://[^\s]+)"
        message = re.sub(regex, ' ', data['message'])
        if data['channel'] != Connection.singleton().details.get_channel():
            return
        regex = r'\b(\w\d{2}\.?\d?)\b'
        codes = re.findall(regex,message)
        for code in codes:
            code = code.capitalize()
            text = self.get_icd(code)
            if (text != 0):
                Connection.singleton().send_back(text, data)
