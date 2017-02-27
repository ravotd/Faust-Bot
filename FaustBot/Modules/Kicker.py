import time
from collections import defaultdict

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.UserList import UserList
from ..Modules.PingObserverPrototype import PingObserverPrototype


class Kicker(PingObserverPrototype):
    warned_users = defaultdict(int)

    def update_on_ping(self, data, connection: Connection):
        for user in UserList.userList:
            if self.get_offline_time(user) < 500:
                self.warned_users[user] = 0
            if self.get_offline_time(user) > 18000 and not user == Connection.singleton().details.get_nick():
                if self.warned_users[user] % 30 == 0:
                    Connection.singleton().send_channel('\001ACTION schüttet ' + user + \
                                                        ' einen Eimer Wasser über den Kopf\001')
                    # Connection.singleton().raw_send("KICK "+Connection.singleton().details.get_channel()+ \
                    # " "+user+" :Zu lang geidlet komm gerne wieder!")
                self.warned_users[user] += 1

    def get_offline_time(self, nick):
        who = nick
        user_provider = UserProvider()
        activity = user_provider.get_activity(who)
        delta = time.time() - activity
        return delta
