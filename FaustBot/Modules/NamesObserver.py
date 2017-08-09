from FaustBot.Communication import Connection
from FaustBot.Modules.MagicNumberObserverPrototype import MagicNumberObserverPrototype
from FaustBot.Modules.UserList import UserList

class NamesObserver(MagicNumberObserverPrototype):
    def __init__(self, user_list: UserList):
        super().__init__()
        self.user_list = user_list

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

