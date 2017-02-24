import datetime
import time

from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from Model.UserProvider import UserProvider
from Model.i18n import i18n


class SeenObserver(PrivMsgObserverPrototype):
    def update_on_priv_msg(self, data):
        if data['message'].find('.seen') == -1:
            return
        who = data['message'].split(' ')[1]
        user_provider = UserProvider()
        activity = user_provider.get_activity(who)
        delta = time.time() - activity
        i18n_server = i18n()
        replacements = {'user': who, 'time': str(datetime.timedelta(seconds=delta))}
        output = i18n_server.get_text('seen', replacements)
        Connection.instance.send_channel(output)
