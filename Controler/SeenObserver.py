from Communication.Connection import Connection
import datetime
import time
from Model.i18n import i18n
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from Model.UserProvider import UserProvider
class SeenObserver(PrivMsgObserverPrototype):
    def update_on_priv_msg(self, data):
        if data['message'].find('.seen') == -1:
            return
        who = data['message'].split(' ')[1]
        userProvider = UserProvider()
        activity = userProvider.get_activity(who)
        delta = time.time()-activity
        i18n_server = i18n()
        replacements = {}
        replacements['user'] = who
        replacements['time'] = str(datetime.timedelta(seconds=delta))
        output = i18n_server.get_text('seen', replacements)
        Connection.instance.send_channel(output)