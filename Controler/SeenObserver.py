from Communication.Connection import Connection
import datetime
import time
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
        Connection.instance.send_channel(data['nick']+":"+who+" sah ich zuletzt vor "+str(datetime.timedelta(seconds=delta)))
