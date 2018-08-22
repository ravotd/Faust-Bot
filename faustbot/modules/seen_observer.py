from faustbot.communication.connection import Connection
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class SeenObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".seen"]

    @staticmethod
    def help():
        return ".seen <nick> - um abzufragen wann <nick> zuletzt hier war"

    def update_on_priv_msg(self, data, connection: Connection):
        pass
        # if data['message'].find('.seen ') == -1:
        #     return
        # who = data['message'].split(' ')[1]
        # user_provider = UserProvider()
        # activity = user_provider.get_activity(who)
        # delta = time.time() - activity
        # i18n_server = i18n()
        # replacements = {'user': who, 'time': str(datetime.timedelta(seconds=delta)), 'asker': data['nick']}
        # output = i18n_server.get_text('seen', replacements=replacements,
        #                               lang=self.config.lang)
        # if not self._is_idented_mod(data, connection):
        #     connection.channel_privmsg(output)
        #     return
        # connection.send_back(output, data)

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data['nick'] in self._config.mods and connection.is_identified(data['nick'])
