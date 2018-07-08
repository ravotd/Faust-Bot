from typing import List

from FaustBot.Communication import Connection
from FaustBot.Model.IRCData import IRCData
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class FreeHugsObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd() -> List[str]:
        return [".hug"]

    @staticmethod
    def help() -> str:
        return ".hug - verteilt Umarmungen"

    def update_on_priv_msg(self, data: IRCData, connection: Connection) -> None:
        if data.is_channel() and data.message.find('.hug') == -1:
            return
        connection.send_back('\001ACTION knuddelt ' + data.nick + '.\001', data)
