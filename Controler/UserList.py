from Controler.JoinObserverPrototype import JoinObserverPrototype
from Controler.KickObserverPrototype import KickObserverPrototype
from Controler.LeaveObserverPrototype import LeaveObserverPrototype


class UserList(JoinObserverPrototype, KickObserverPrototype, LeaveObserverPrototype):
    #todo for Multi Channel Faust Add Channel descriptor here
    userList = []

    def update_on_kick(self, data):
        self.userList.remove(data['nick'])

    def update_on_leave(self, data):
        self.userList.remove(data['nick'])


    def update_on_join(self, data):
        self.userList.append(data['nick'])
        print('joined: ' + data['nick'] + '\r\n')
        print('userList: ')
        print(self.userList)