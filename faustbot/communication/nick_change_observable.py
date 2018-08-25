import _thread

from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.nick_change_observer_prototype import NickChangeObserverPrototype


class NickChangeObservable(Observable):
    def notify_observer(self, observer: NickChangeObserverPrototype, data: IRCData, connection):
        _thread.start_new_thread(observer.__class__.update_on_nick_change, (observer, data, connection))
