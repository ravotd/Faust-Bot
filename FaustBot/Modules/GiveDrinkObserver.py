import random
from typing import List

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.IRCData import IRCData
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from getraenke import getraenke


class GiveDrinkObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd() -> List[str]:
        return [".drink"]

    @staticmethod
    def help() -> str:
        return ".drink - schenkt Getränke aus"

    def update_on_priv_msg(self, data: IRCData, connection: Connection) -> None:
        if data.is_channel() and data.message.find('.drink') == -1:
            return
        connection.send_back('\001ACTION schenkt ' + data.nick + ' ' + random.choice(getraenke) + ' ein.\001', data)
