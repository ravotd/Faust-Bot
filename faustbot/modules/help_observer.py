from typing import List

from faustbot.communication import connection
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class HelpObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd() -> List[str]:
        return [".help"]

    @staticmethod
    def help() -> str:
        return ".help - zeigt Hilftexte aller Module an"

    def update_on_priv_msg(self, data: IRCData, connection: connection) -> None:
        msg = data.message
        if not msg.startswith(".help"):
            return

        if data.is_channel():
            all_cmd = []
            for observer in connection.priv_msg_observable.get_observer():
                cmds = observer.cmd()
                if cmds is not None:
                    all_cmd.extend(cmds)
            msg = ", ".join(all_cmd)
            msg = "Bekannte Befehle: " + msg + ". Für Details per Query .help ."
            connection.send_back(msg, data)
        else:
            all_help = [m.help() for m in connection.priv_msg_observable.get_observer()]
            for help_msg in all_help:
                if help_msg is not None:
                    connection.send_back(help_msg, data)
