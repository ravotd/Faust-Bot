import _thread

from Communication.Observable import Observable

class JoinObservable(Observable):

    def input(self, raw_data):
        data = {}
        data['raw'] = raw_data
        data['nick'] = raw_data.split('!')[0][1:]
        data['channel'] = raw_data.split('JOIN ')[1].split(' :')[0]
        data['raw_nick'] = raw_data.split(' JOIN')[0][1:]
        self.notifyObservers(data)

    def notifyObservers(self, data):
         for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_join, (observer, data))
