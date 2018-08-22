from typing import List

from faustbot.communication import connection
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class FreeHugsObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd() -> List[str]:
        return [".hug"]

    @staticmethod
    def help() -> str:
        return ".hug - verteilt Umarmungen"

    def update_on_priv_msg(self, data: IRCData, connection: connection) -> None:
        if data.is_channel() and data.message.find('.hug') == -1:
            return
        connection.send_back('\001ACTION knuddelt ' + data.nick + '.\001', data)
