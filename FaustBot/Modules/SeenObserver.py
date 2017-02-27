import datetime
import time

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from ..Model.i18n import i18n


class SeenObserver(PrivMsgObserverPrototype):
    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.seen') == -1:
            return
        who = data['message'].split(' ')[1]
        user_provider = UserProvider()
        activity = user_provider.get_activity(who)
        delta = time.time() - activity
        i18n_server = i18n()
        replacements = {'user': who, 'time': str(datetime.timedelta(seconds=delta))}
        output = i18n_server.get_text('seen', replacements=replacements,
                                      lang=self.config.lang)
        connection.send_channel(output)
