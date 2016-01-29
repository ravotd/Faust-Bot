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

    def input_names(self, raw_data):
        i = 0
        data = {}
        data[i] = {}
        data[i]['raw_data'] = raw_data
        data[i]['channel'] = raw_data.split(' = ')[1].split(' :')[0]
        nicks = raw_data.split('353')[1].split('\n')[0].split(' :')[1].split(' ')
        for nick in nicks:
            nick = nick.strip('\r')
            nick = nick.strip('\n')
            nick = nick.strip('@')
            nick = nick.strip('+')
            nick = nick.strip('~')
            nick = nick.strip('%')
            data[i]['nick'] = nick
            self.notifyObservers(data[i])
            i += 1
            data[i] = {}
            data[i]['raw_data'] = data[i-1]['raw_data']
            data[i]['channel'] = data[i-1]['channel']


    def notifyObservers(self, data):
         for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_join, (observer, data))
