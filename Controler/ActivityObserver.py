from Communication.Connection import Connection
from Controler.JoinObserverPrototype import JoinObserverPrototype
from Model.UserProvider import UserProvider

from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class AcitivityObserver(PrivMsgObserverPrototype, JoinObserverPrototype):
    """
    A Class only reacting to pings
    """

    def update_on_join(self, data):
        users = UserProvider()
        if data['channel'] == Connection.singleton().details.get_channel():
            users.set_active(data['nick'])

    def update_on_priv_msg(self, data):
        users = UserProvider()
        if data['channel'] == Connection.singleton().details.get_channel():
            users.set_active(data['nick'])
            users.add_characters(data['nick'],len(data['message']))

