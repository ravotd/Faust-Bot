from FaustBot.Modules.JoinObserverPrototype import JoinObserverPrototype
from FaustBot.Modules.ModuleType import ModuleType
from ..Modules.KickObserverPrototype import KickObserverPrototype
from ..Modules.LeaveObserverPrototype import LeaveObserverPrototype
from ..Modules.NickChangeObserverPrototype import NickChangeObserverPrototype


class UserList(JoinObserverPrototype, KickObserverPrototype, LeaveObserverPrototype, NickChangeObserverPrototype):
    def __init__(self):
        super().__init__()
        self.userList = []

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_JOIN, ModuleType.ON_KICK, ModuleType.ON_LEAVE, ModuleType.ON_NICK_CHANGE]

    def update_on_kick(self, data, connection):
        self.userList.remove(data['nick'])
        print(self.userList)

    def update_on_leave(self, data, connection):
        self.userList.remove(data['nick'])
        print(self.userList)

    def update_on_join(self, data, connection):
        try:
            self.userList.remove(data['nick'])
        except Exception:
            1+1               
        self.userList.append(data['nick'])
        print(self.userList)

    def update_on_nick_change(self, data, connection):
        self.userList.remove(data['old_nick'])
        self.userList.append(data['new_nick'])
        print(self.userList)
