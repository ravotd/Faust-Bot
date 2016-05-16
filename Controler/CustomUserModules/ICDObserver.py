from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype
import re
import urllib
from urllib import request
import html

class ICDObserver(PrivMsgObserverPrototype):

    def update_on_priv_msg(self, data):
        codes = re.findall('(^|\s)(\w\d{2}\.?\d?)(\s|$)', data['message'])
        for code in codes:
            code = code[1].capitalize()
            if code.find('.') == -1:
                code = code + '.-'
            url = 'http://www.icd-code.de/icd/code/' + code + '.html'
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
                req = urllib.request.Request(url, None, headers)
                resource = urllib.request.urlopen(req)
                encoding = 'iso-8859-1'
                content =  resource.read().decode(encoding, errors='replace')
                titleRE = re.compile('<title>ICD-10-GM-2016\s(.+?)\sICD10\s</title>')
                title = titleRE.search(content).group(1)
                title = html.unescape(title)
                title = title.replace('\n', ' ').replace('\r', '')
                print(title)
                Connection.singleton().send_channel(title + ': ' + url)
            except Exception as exc:
                print(exc)
                pass

