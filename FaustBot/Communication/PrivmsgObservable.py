import _thread

from FaustBot.Communication.Observable import Observable


class PrivmsgObservable(Observable):
    def input(self, raw_data, connection):
        data = {'raw': raw_data, 'nick': raw_data.split('!')[0][1:],
                'channel': raw_data.split('PRIVMSG ')[1].split(' :')[0],
                'raw_nick': raw_data.split(' PRIVMSG')[0][1:]}
        # 12 = :<raw_nick> PRIVMSG <channel> :<message>
        data['message'] = raw_data[data['raw_nick'].__len__() + data['channel'].__len__() + 12:]
        data['command'] = 'irgendwas, das mit . oder .. anfängt oder so... oder das sollen module checken?'

        self.notify_observers(data, connection)

    def notify_observers(self, data, connection):
        for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_priv_msg, (observer, data, connection))
