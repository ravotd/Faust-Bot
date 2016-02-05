import _thread

from Communication.Observable import Observable

class NickChangeObservable(Observable):

    def input(self, raw_data):
        data = {}
        data['raw'] = raw_data
        data['old_nick'] = raw_data.split('!')[0][1:]
        data['new_nick'] = raw_data.split('NICK ')[1].split(':')[1]
        data['raw_nick'] = raw_data.split(' NICK')[0][1:]
        self.notifyObservers(data)

    def notifyObservers(self, data):
         for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_nick_change, (observer, data))
