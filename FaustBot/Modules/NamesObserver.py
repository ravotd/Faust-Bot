from FaustBot.Communication import Connection
from FaustBot.Modules.MagicNumberObserverPrototype import MagicNumberObserverPrototype

class NamesObserver(MagicNumberObserverPrototype):

    def update_on_magic_number(self, data, connection):
        if data['raw'].find('353') == -1:
            return
        print('353 detected1')
        self.input_names(data, connection)
        
    def input_names(self, raw_data, connection: Connection):
        i = 0
        data = {i: {}}
        raw_data = raw_data['raw']
        data[i]['raw_data'] = raw_data
        if raw_data.find(' = ') != -1:
            data[i]['channel'] = raw_data.split(' = ')[1].split(' :')[0]
        if raw_data.find(' @ ') != -1:
            data[i]['channel'] = raw_data.split(' @ ')[1].split(' :')[0]
        if raw_data.find(' * ') != -1:
            data[i]['channel'] = raw_data.split(' * ')[1].split(' :')[0]
        nicks = raw_data.split('353')[1].split('\n')[0].split(' :')[1].split(' ')
        for nick in nicks:
            nick = nick.strip('\r')
            nick = nick.strip('\n')
            nick = nick.strip('@')
            nick = nick.strip('+')
            nick = nick.strip('~')
            nick = nick.strip('%')
            data[i]['nick'] = nick
            connection.join_observable.notify_observers(data[i], connection)
            i += 1
            data[i] = {}
            data[i]['raw_data'] = data[i - 1]['raw_data']
            data[i]['channel'] = data[i - 1]['channel']
