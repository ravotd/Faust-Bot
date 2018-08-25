import _thread

from faustbot.communication.connection import Connection
from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class PrivmsgObservable(Observable):
    def notify_observer(self, observer: PrivMsgObserverPrototype, data: IRCData, connection: Connection):
        _thread.start_new_thread(observer.__class__.update_on_priv_msg, (observer, data, connection))
