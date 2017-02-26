from FaustBot.Modules.JoinObserverPrototype import JoinObserverPrototype
from FaustBot.Modules.ModuleType import ModuleType
from ..Modules.KickObserverPrototype import KickObserverPrototype
from ..Modules.LeaveObserverPrototype import LeaveObserverPrototype
from ..Modules.NickChangeObserverPrototype import NickChangeObserverPrototype


class UserList(JoinObserverPrototype, KickObserverPrototype, LeaveObserverPrototype, NickChangeObserverPrototype):
    # todo for Multi Channel Faust Add Channel descriptor here
    userList = []

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_JOIN, ModuleType.ON_KICK, ModuleType.ON_LEAVE, ModuleType.ON_NICK_CHANGE]

    def update_on_kick(self, data):
        self.userList.remove(data['nick'])

    def update_on_leave(self, data):
        self.userList.remove(data['nick'])

    def update_on_join(self, data):
        self.userList.append(data['nick'])

    def update_on_nick_change(self, data):
        self.userList.remove(data['old_nick'])
        self.userList.append(data['new_nick'])
