from faustbot.communication import connection
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class LoveAndPeaceObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".peace"]

    @staticmethod
    def help():
        return ".peace - sorgt für Frieden"

    def update_on_priv_msg(self, data: IRCData, connection: connection):
        if data.message.find('.peace') == -1:
            return
        connection.send_back('\001ACTION hüpft durch den Raum, schmeißt Blumen um sich und singt: \"Love and '
                             'Peace, wir haben uns alle lieb..!\".\001', data)
