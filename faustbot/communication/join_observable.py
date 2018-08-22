import _thread

from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData


class JoinObservable(Observable):
    def notify_observers(self, data: IRCData, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_join, (observer, data, connection))