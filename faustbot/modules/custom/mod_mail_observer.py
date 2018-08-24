from faustbot.communication.connection import Connection
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class ModmailObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".modmail"]

    @staticmethod
    def help():
        return ".modmail <msg> - Sendet allen Moderatoren <msg> per PN"

    def update_on_priv_msg(self, data: IRCData, connection: Connection):
        if data.message.find('.modmail') == -1:
            return
        channel = data.channel
        mods = connection.config.get_channel_by_name(channel)
        message = data.message.split('.modmail ')[1]
        for mod in mods:
            connection.user_privmsg(mod, data.nick + ' meldet: ' + message)
