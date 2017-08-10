from FaustBot.Communication import Connection
from FaustBot.Modules.MagicNumberObserverPrototype import MagicNumberObserverPrototype
from FaustBot.Modules.UserList import UserList
from FaustBot.Modules.PingObserverPrototype import PingObserverPrototype
from FaustBot.Modules.ModuleType import ModuleType

class NamesObserver(MagicNumberObserverPrototype, PingObserverPrototype):
    def __init__(self, user_list: UserList):
        super().__init__()
        self.user_list = user_list
        self.pings_seen = 1

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_MAGIC_NUMBER, ModuleType.ON_PING]

    def update_on_magic_number(self, data, connection):
        if data['raw'].find('353') == -1:
            return
        print('353 detected1')
        self.input_names(data, connection)
        
    def input_names(self, data, connection: Connection):
        self.user_list.clear_list()
        nicks = data['raw'].split('353')[1].split('\n')[0].split(' :')[1].split(' ')
        for nick in nicks:
            nick = nick.strip('\r')
            nick = nick.strip('\n')
            nick = nick.strip('@')
            nick = nick.strip('+')
            nick = nick.strip('~')
            nick = nick.strip('%')
            self.user_list.__class__.update_on_join(self.user_list, {'nick': nick}, connection)

    def update_on_ping(self, data, connection: Connection):
        if self.pings_seen % 90 == 0: # 90 * 2 min = 3 Stunden
            connection.raw_send('NAMES ' + connection.details.get_channel())
            self.pings_seen += 1
