import _thread

from Communication.Observable import Observable

class PrivmsgObservable(Observable):

    def input(self, raw_data):
        data = {}
        data['raw'] = raw_data
        data['nick'] = raw_data.split('!')[0][1:]
        data['channel'] = raw_data.split('PRIVMSG ')[1].split(' :')[0]
        data['raw_nick'] = raw_data.split(' PRIVMSG')[0][1:]
        # 12 = :<raw_nick> PRIVMSG <channel> :<message>
        data['message'] = raw_data[data['raw_nick'].__len__() + data['channel'].__len__() + 12:]
        data['command'] = 'irgendwas, das mit . oder .. anfängt oder so... oder das sollen module checken?'


        self.notifyObservers(data)

    def notifyObservers(self, data):
         for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_priv_msg, (observer, data))

