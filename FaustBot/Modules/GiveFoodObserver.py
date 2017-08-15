from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from essen import essen
import random


class GiveFoodObserver(PrivMsgObserverPrototype):

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.food') == -1:
            return
        connection.send_back('\001ACTION tischt ' + data['nick'] + ' ' + random.choice(essen) + ' auf.\001', data)
