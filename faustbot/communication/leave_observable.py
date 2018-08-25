import _thread

from faustbot.communication.connection import Connection
from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.leave_observer_prototype import LeaveObserverPrototype


class LeaveObservable(Observable):
    def notify_observer(self, observer: LeaveObserverPrototype, data: IRCData, connection: Connection):
        _thread.start_new_thread(observer.__class__.update_on_leave, (observer, data, connection))
