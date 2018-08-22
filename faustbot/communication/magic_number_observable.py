import _thread

from faustbot.communication.observable import Observable
from faustbot.model.irc_data import IRCData


class MagicNumberObservable(Observable):
    def notify_observers(self, data: IRCData, connection):
        for observer in self._observers:
            try:
                _thread.start_new_thread(observer.__class__.update_on_magic_number, (observer, data, connection))
            except Exception:
                import traceback
                print(traceback.format_exc())
