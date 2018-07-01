import _thread

from FaustBot.Communication.Observable import Observable
from FaustBot.Model.IRCData import IRCData


class MagicNumberObservable(Observable):
    def notify_observers(self, data: IRCData, connection):
        for observer in self._observers:
            try:
                _thread.start_new_thread(observer.__class__.update_on_magic_number, (observer, data, connection))
            except Exception:
                import traceback
                print(traceback.format_exc())
