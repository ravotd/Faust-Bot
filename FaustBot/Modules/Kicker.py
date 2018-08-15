import random
import time
from collections import defaultdict

from FaustBot.Communication.Connection import Connection
from FaustBot.Model.RemoteUser import RemoteUser
from FaustBot.Model.UserProvider import UserProvider
from FaustBot.Modules.UserList import UserList
from getraenke import getraenke
from ..Modules.PingObserverPrototype import PingObserverPrototype


class Kicker(PingObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self, user_list: UserList, idle_time: int):
        super().__init__()
        self.idle_time = idle_time
        self.user_list = user_list
        self.warned_users = {}

    def update_on_ping(self, data, connection: Connection):
        for channel, users in self.user_list.userList.values():
            for user in users:
                self.check_user_idle_time(channel, user, connection)


    @staticmethod
    def get_offline_time(nick: str, channel: str):
        user_provider = UserProvider()
        activity = user_provider.get_activity(nick, channel)
        delta = time.time() - activity
        return delta

    def check_user_idle_time(self, channel: str, user: RemoteUser, connection: Connection):
        offline_time = Kicker.get_offline_time(user)
        if offline_time < self.idle_time:
            self.warned_users[user] = 0
        host = self.user_list.userList.get(user).host
        if offline_time > self.idle_time \
                and not user == connection.config.get_nick() \
                and 'freenode/staff' not in host and 'freenode/utility-bot' not in host:
            if self.warned_users[user] % 30 == 0:
                connection.channel_privmsg(
                    '\001ACTION schenkt ' + user + ' ' + random.choice(getraenke) + ' ein.\001')
            self.warned_users[user] += 1
            if self.warned_users[user] % 29 == 0:
                connection.raw_send("KICK " + connection.config.get_channel() + " " + user +
                                    " :Zu lang geidlet, komm gerne wieder!")
