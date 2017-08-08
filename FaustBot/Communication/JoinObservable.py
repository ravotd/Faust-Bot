import _thread

from FaustBot.Communication.Observable import Observable


class JoinObservable(Observable):
    def input(self, raw_data, connection):
        data = {'raw': raw_data, 'nick': raw_data.split('!')[0][1:],
                'channel': raw_data.split('JOIN ')[1].split(' :')[0], 'raw_nick': raw_data.split(' JOIN')[0][1:]}
        self.notify_observers(data, connection)


    def notify_observers(self, data, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_join, (observer, data, connection))
