from faustbot.communication.connection import Connection
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class ModmailObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".modmail"]

    @staticmethod
    def help():
        return ".modmail <msg> - Sendet allen Moderatoren <msg> per PN"

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.modmail') == -1:
            return
        mods = connection.config.get_mods()
        print(mods)
        message = data['message'].split('.modmail ')[1]
        for mod in mods:
            connection.user_privmsg(mod, data['nick'] + ' meldet: ' + message)