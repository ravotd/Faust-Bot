from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from getraenke import getraenke
import random

class GiveDrinkObserver(PrivMsgObserverPrototype):

    def update_on_priv_msg(self, data):
        if data['message'].find('.drink') == -1:
            print("Test42")
            return
        Connection.singleton().send_channel('\001ACTION schenkt ' + data['nick'] + ' ' + random.choice(getraenke) + ' ein.\001')
        print("Test")