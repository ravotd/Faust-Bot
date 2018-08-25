import _thread

from faustbot.communication.connection import Connection
from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.join_observer_prototype import JoinObserverPrototype


class JoinObservable(Observable):
    def notify_observer(self, observer: JoinObserverPrototype, data: IRCData, connection: Connection):
            _thread.start_new_thread(observer.__class__.update_on_join, (observer, data, connection))
