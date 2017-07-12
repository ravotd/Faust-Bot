import random
import time
from collections import defaultdict

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.UserList import UserList
from getraenke import getraenke
from ..Modules.PingObserverPrototype import PingObserverPrototype


class Kicker(PingObserverPrototype):
    warned_users = defaultdict(int)

    def update_on_ping(self, data, connection: Connection):
        for user in UserList.userList:
            if self.get_offline_time(user) < 500:
                self.warned_users[user] = 0
            if self.get_offline_time(user) > 18000 and not user == connection.details.get_nick():
                if self.warned_users[user] % 30 == 0:
                    connection.send_channel(
                        '\001ACTION schenkt ' + user + ' ' + random.choice(getraenke) + ' ein.\001')
                self.warned_users[user] += 1
                if self.warned_users[user] % 29 == 0:
                    connection.raw_send("KICK " + connection.details.get_channel() +
                                        " " + user + " :Zu lang geidlet, komm gerne wieder!")

    def get_offline_time(self, nick):
        who = nick
        user_provider = UserProvider()
        activity = user_provider.get_activity(who)
        delta = time.time() - activity
        return delta
