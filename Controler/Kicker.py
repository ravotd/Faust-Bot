from Controler.PingObserverPrototype import PingObserverPrototype
from Controler.UserList import UserList
from Communication.Connection import Connection
from Model.UserProvider import UserProvider
from collections import defaultdict
from getraenke import getraenke
import time
import random
class Kicker(PingObserverPrototype):

    warned_users = defaultdict(int)

    def update_on_ping(self, data):
        for user in UserList.userList:
            if self.getOfflineTime(user) < 500:
                self.warned_users[user] = 0
            if self.getOfflineTime(user) > 18000 and not user == Connection.singleton().details.get_nick():
                if self.warned_users[user] % 30 == 0:
                    Connection.singleton().send_channel('\001ACTION schenkt ' + user + ' '+random.choice(getraenke)+' ein.\001' )
                self.warned_users[user] += 1
                if self.warned_users[user] % 29 == 0:
                    Connection.singleton().raw_send("KICK "+Connection.singleton().details.get_channel()+ \
                     " "+user+" :Zu lang geidlet, komm gerne wieder!")

    def getOfflineTime(self, nick):
        who = nick
        userProvider = UserProvider()
        activity = userProvider.get_activity(who)
        delta = time.time()-activity
        return delta
