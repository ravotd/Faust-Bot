import random
import time

from FaustBot.Communication.Connection import Connection
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
        self._still_working = False

    def update_on_ping(self, data, connection: Connection):
        if self._still_working:
            return
        self._still_working = True
        for channel in self.warned_users.keys():
            self.check_channel_users(channel, connection)
        self._clean_warned_users()
        self._still_working = False

    def check_channel_users(self, channel: str, connection: Connection):
        for user in self.user_list.userList[channel].keys():
            offline_time = Kicker.get_offline_time(user)
            if offline_time < self.idle_time:
                self._set_user_counter(channel, user, 0)
            host = self.user_list.get_user(channel, user)
            if offline_time > self.idle_time \
                    and not user == connection.config.get_nick() \
                    and 'freenode/staff' not in host \
                    and 'freenode/utility-bot' not in host:
                counter = self._get_user_counter(channel, user)
                if counter % 30 == 0:
                    connection.channel_privmsg(
                        '\001ACTION schenkt ' + user + ' ' + random.choice(getraenke) + ' ein.\001')
                else:
                    self._inc_user_counter(channel, user)
                    counter = self._get_user_counter(channel, user)
                    if counter % 29 == 0:
                        connection.raw_send("KICK " + connection.config.get_channel() + " " + user +
                                            " :Zu lang geidlet, komm gerne wieder!")

    def _get_user_counter(self, channel: str, user: str):
        if channel not in self.warned_users:
            return None
        channel_users = self.warned_users[channel]
        return channel_users.get(user, None)

    def _set_user_counter(self, channel: str, user: str, count: int):
        if channel not in self.warned_users:
            self.warned_users[channel] = {}
        channel_users = self.warned_users[channel]
        channel_users[user] = count

    def _inc_user_counter(self, channel: str, user: str):
        counter = self._get_user_counter(channel, user)
        if counter is not None:
            counter = counter + 1
        else:
            counter = 1
        self._set_user_counter(channel, user, counter)

    def _clean_warned_users(self):
        to_del_channel = []
        for channel, users in self.warned_users.items():
            to_del_users = []
            for user, count in users.items():
                if count is None or count == 0:
                    to_del_users.append(user)
            Kicker.del_elements(users, to_del_users)
            if len(users) == 0:
                to_del_channel.append(channel)
        Kicker.del_elements(self.warned_users, to_del_channel)

    @staticmethod
    def del_elements(d: dict, to_del: list):
        for td in to_del:
            del d[td]

    @staticmethod
    def get_offline_time(nick):
        who = nick
        user_provider = UserProvider()
        activity = user_provider.get_activity(who)
        delta = time.time() - activity
        return delta
