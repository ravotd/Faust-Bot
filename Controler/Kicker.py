from Controler.PingObserverPrototype import PingObserverPrototype
from Controler.UserList import UserList
from Communication.Connection import Connection
from Model.UserProvider import UserProvider

import time

class Kicker(PingObserverPrototype):
    def update_on_ping(self, data):
        for user in UserList.userList:
            if self.getOfflineTime(user) > 18000 and not user == Connection.singleton().details.get_nick():
                Connection.singleton().raw_send("KICK "+Connection.singleton().details.get_channel()+" "+user+" :Zu lang geidlet komm gerne wieder!")

    def getOfflineTime(self, nick):
        who = nick
        userProvider = UserProvider()
        activity = userProvider.get_activity(who)
        delta = time.time()-activity
        return delta
