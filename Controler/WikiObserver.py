from wikipedia import wikipedia
from Model.i18n import i18n

from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class WikiObserver(PrivMsgObserverPrototype):

    def update_on_priv_msg(self, data):
        if data['message'].find('.w ') == -1:
            return
        i18n_server = i18n()
        w = wikipedia.set_lang(i18n_server.get_text('wiki_lang'))
        q = data['message'].split(' ')
        query = ''
        for word in q:
            if word.strip() != '.w':
                query += word + ' '
        w = wikipedia.search(query)
        if w.__len__() == 0:
            Connection.singleton().send_channel(data['nick'] + ', ' + i18n_server.get_text('wiki_fail'))
            return
        try:
            page = wikipedia.WikipediaPage(w.pop(0))
        except wikipedia.DisambiguationError as error:
            print('disambiguation page')
            page = wikipedia.WikipediaPage(error.args[1][0])
        Connection.singleton().send_channel(data['nick'] + ' ' + page.url)
        index = page.summary.find('. ')
        if index == -1 or index > 230:
            Connection.singleton().send_channel(page.summary[0:230])
        else:
            Connection.singleton().send_channel(page.summary[0:index+1])
