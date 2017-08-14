import random
import time
from collections import defaultdict

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.UserList import UserList
from getraenke import getraenke
from ..Modules.PingObserverPrototype import PingObserverPrototype


class Kicker(PingObserverPrototype):
    def __init__(self, user_list: UserList, idle_time: int):
        super().__init__()
        self.idle_time = idle_time
        self.user_list = user_list
        self.warned_users = defaultdict(int)

    def update_on_ping(self, data, connection: Connection):
        for user in self.user_list.userList:
            offline_time = Kicker.get_offline_time(user)
            if offline_time < 36000:
                self.warned_users[user] = 0
            # 36000s (= 1h) to test instead of 18000s (= 5h)
            if offline_time > self.idle_time and not user == connection.details.get_nick() and not user == "Sigyn":
                if self.warned_users[user] % 30 == 0:
                    connection.send_channel(
                        '\001ACTION schenkt ' + user + ' ' + random.choice(getraenke) + ' ein.\001')
                self.warned_users[user] += 1
                if self.warned_users[user] % 29 == 0:
                    connection.raw_send("KICK " + connection.details.get_channel() + " " + user +
                                        " :Zu lang geidlet, komm gerne wieder!")

    @staticmethod
    def get_offline_time(nick):
        who = nick
        user_provider = UserProvider()
        activity = user_provider.get_activity(who)
        delta = time.time() - activity
        return delta
