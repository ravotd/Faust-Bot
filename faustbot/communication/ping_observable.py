import _thread

from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.ping_observer_prototype import PingObserverPrototype


class PingObservable(Observable):
    def notify_observer(self, observer: PingObserverPrototype, data: IRCData, connection):
        _thread.start_new_thread(observer.__class__.update_on_ping, (observer, data, connection))
