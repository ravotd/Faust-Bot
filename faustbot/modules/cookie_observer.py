import random
from typing import List

from faustbot.communication import connection
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype

kekse = ['einen Schokoladenkeks', 'einen Vanillekeks', 'einen Doppelkeks', 'keinen Keks',
         'einen Keks', 'einen Erdbeerkeks', 'einen Schokoladen Cheescake keks',
         'einen Glückskeks', 'einen Scherzkeks', 'einen Unglückskeks']


class GiveCookieObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd() -> List[str]:
        return [".cookie"]

    @staticmethod
    def help() -> str:
        return ".cookie - verteilt kekse; oder auch nicht"

    def update_on_priv_msg(self, data: IRCData, connection: connection) -> None:
        if data.is_channel() and data.message.find('.cookie') == -1:
            return
        connection.send_back('\001ACTION schenkt ' + data.nick + ' ' + random.choice(kekse) + '.\001', data)
