from wikipedia import wikipedia

from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class WikiObserver(PrivMsgObserverPrototype):

    def update_on_priv_msg(self, data):
        if data['message'].find('.w') == -1:
            return
        w = wikipedia.set_lang('de')
        q = data['message'].split(' ')
        query = ''
        for word in q:
            if word != '.w':
                query += word + ' '
        w = wikipedia.search(query)
        print(query)
        if w.__len__() == 0:
            Connection.singleton().send_channel(data['nick'] +
                ', in Wikipedia finde ich dazu nichts. Magst du einen Artikel dazu schreiben?')
            return
        page = wikipedia.WikipediaPage(w.pop(0))
        Connection.singleton().send_channel(data['nick'] + ' ' + page.url)
        Connection.singleton().send_channel(page.summary)
