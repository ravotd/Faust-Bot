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
        i = 1
        data ={}
        data['raw_data'] = raw_data
        data['channel'] = raw_data.split(' = ')[1].split(' :')[0]
        nicks = raw_data.split('353')[1].split('\n')[0].split(' :')[1].split(' ')
        for nick in nicks:
            nick = nick.strip('\r')
            nick = nick.strip('\n')
            nick = nick.strip('@')
            nick = nick.strip('+')
            nick = nick.strip('~')
            nick = nick.strip('%')
            data['nick'] = nick
            print('join on names')
            print (i)
            i = i + 1
            print(data)
            print('end join on names')
            self.notifyObservers(data)


    def notifyObservers(self, data):
         for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_join, (observer, data))
