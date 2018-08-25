import _thread

from faustbot.communication.connection import Connection
from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.magic_number_observer_prototype import MagicNumberObserverPrototype


class MagicNumberObservable(Observable):
    def notify_observer(self, observer: MagicNumberObserverPrototype, data: IRCData, connection: Connection):
        _thread.start_new_thread(observer.__class__.update_on_magic_number, (observer, data, connection))
