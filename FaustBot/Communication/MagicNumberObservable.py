import _thread

from FaustBot.Communication.Observable import Observable


class MagicNumberObservable(Observable):
    def input(self, raw_data, connection):
        data = {}
        data['raw'] = raw_data
        
        self.notify_observers(data, connection)

    def notify_observers(self, data, connection):
        for observer in self._observers:
            try:
                _thread.start_new_thread(observer.__class__.update_on_magic_number, (observer, data, connection))
            except Exception:
                import traceback
                print (traceback.format_exc())
