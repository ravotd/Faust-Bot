from Controler.JoinObserverPrototype import JoinObserverPrototype
from Controler.KickObserverPrototype import KickObserverPrototype
from Controler.LeaveObserverPrototype import LeaveObserverPrototype
from Controler.NickChangeObserverPrototype import NickChangeObserverPrototype


class UserList(JoinObserverPrototype, KickObserverPrototype, LeaveObserverPrototype, NickChangeObserverPrototype):
    #todo for Multi Channel Faust Add Channel descriptor here
    userList = []

    def update_on_kick(self, data):
        self.userList.remove(data['nick'])

    def update_on_leave(self, data):
        self.userList.remove(data['nick'])


    def update_on_join(self, data):
        self.userList.append(data['nick'])

    def update_on_nick_change(self, data):
        self.userList.remove(data['old_nick'])
        self.userList.append(data['new_nick'])
