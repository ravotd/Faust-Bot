import random
from typing import List

from essen import essen
from faustbot.communication.connection import Connection
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class GiveFoodObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd() -> List[str]:
        return [".food"]

    @staticmethod
    def help() -> str:
        return ".food - gibt etwas zu essen aus"

    def update_on_priv_msg(self, data: IRCData, connection: Connection) -> None:
        if data.is_channel() and data.message.find('.food') == -1:
            return
        connection.send_back('\001ACTION tischt ' + data.nick + ' ' + random.choice(essen) + ' auf.\001', data)
