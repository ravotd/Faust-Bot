import _thread

from faustbot.communication.connection import Connection
from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.kick_observer_prototype import KickObserverPrototype


class KickObservable(Observable):
    def notify_observer(self, observer: KickObserverPrototype, data: IRCData, connection: Connection):
        _thread.start_new_thread(observer.__class__.update_on_kick, (observer, data, connection))
