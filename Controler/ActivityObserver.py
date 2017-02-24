from Communication.Connection import Connection
from Controler.JoinObserverPrototype import JoinObserverPrototype
from Controler.NickChangeObserverPrototype import NickChangeObserverPrototype
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from Model.UserProvider import UserProvider


class AcitivityObserver(PrivMsgObserverPrototype, JoinObserverPrototype, NickChangeObserverPrototype):
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
            users.add_characters(data['nick'], len(data['message']))

    def update_on_nick_change(self, data):
        users = UserProvider()
        users.set_active(data['new_nick'])
