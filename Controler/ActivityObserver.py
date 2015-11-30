from Communication.Connection import Connection
from Model.UserProvider import UserProvider

from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class AcitivityObserver(PrivMsgObserverPrototype):
    """
    A Class only reacting to pings
    """
    def update_on_priv_msg(self, data):
        users = UserProvider()
        if data['channel'] == Connection.singleton().details.get_channel():
            users.set_active(data['nick'])
            users.add_characters(data['nick'],len(data['message']))

