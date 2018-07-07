from FaustBot.Communication import Connection
from FaustBot.Model.IRCData import IRCData
from FaustBot.Model.RemoteUser import RemoteUser
from FaustBot.Modules.MagicNumberObserverPrototype import MagicNumberObserverPrototype
from FaustBot.Modules.ModuleType import ModuleType
from FaustBot.Modules.PingObserverPrototype import PingObserverPrototype
from FaustBot.Modules.UserList import UserList


class WhoObserver(MagicNumberObserverPrototype, PingObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self, user_list: UserList):
        super().__init__()
        self.user_list = user_list
        self.pings_seen = 1

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_MAGIC_NUMBER, ModuleType.ON_PING]

    def update_on_magic_number(self, data: IRCData, connection):
        if data.command == '352':  # RPL_WHOREPLY
            self.input_who(data, connection)

    def input_who(self, data, connection: Connection):
        # target #channel user host server nick status :0 gecos
        target, channel, user, host, server, nick, *ign = data.message.split(' ')
        self.user_list.update_user(RemoteUser(nick, user, host), channel)

    def update_on_ping(self, data, connection: Connection):
        for c in connection.config.channel:
            if self.pings_seen % 90 == 0:  # 90 * 2 min = 3 Stunden
                connection.raw_send('WHO ' + c.name)
                self.pings_seen += 1
