import random
from typing import List

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.IRCData import IRCData
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from essen import essen


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
