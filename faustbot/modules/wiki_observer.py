from wikipedia import wikipedia

from faustbot.communication.connection import Connection
from faustbot.model.i18n import i18n
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype
from faustbot.util import logging


class WikiObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".w"]

    @staticmethod
    def help():
        return ".w <term> - fragt Wikipediaartikel zu <term> ab"

    def update_on_priv_msg(self, data: IRCData, connection: Connection):
        if data.message.find('.w ') == -1:
            return
        lang = connection.config.get_channel_by_name(data.channel).lang
        i18n_server = i18n()
        w = wikipedia.set_lang(i18n_server.get_text('wiki_lang', lang=lang))
        q = data.message.split(' ')
        query = ''
        for word in q:
            if word.strip() != '.w':
                query += word + ' '
        w = wikipedia.search(query)
        if len(w) == 0:  # TODO BUG BELOW, ERROR MESSAGE NOT SHOWN!
            connection.send_back(data.nick + ', ' +
                                 i18n_server.get_text('wiki_fail', lang=lang),
                                 data)
            return
        try:
            page = wikipedia.WikipediaPage(w.pop(0))
        except wikipedia.DisambiguationError as error:
            logging.get_logger(self.__name__).debug('disambiguation page for query: %s', query)
            page = wikipedia.WikipediaPage(error.args[1][0])
        connection.send_back(data['nick'] + ' ' + page.url, data)
        index = 51 + page.summary[50:350].rfind('. ')
        if index == 50 or index > 230:
            index = page.summary[0:350].rfind(' ')
            connection.send_back(page.summary[0:index], data)
        else:
            connection.send_back(page.summary[0:index], data)
