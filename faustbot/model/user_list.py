from typing import Union

from faustbot.communication.connection import Connection
from faustbot.model.irc_data import IRCData
from faustbot.model.remote_user import RemoteUser
from faustbot.modules.module_type import ModuleType
from faustbot.modules.prototypes.join_observer_prototype import JoinObserverPrototype
from faustbot.modules.prototypes.kick_observer_prototype import KickObserverPrototype
from faustbot.modules.prototypes.leave_observer_prototype import LeaveObserverPrototype
from faustbot.modules.prototypes.nick_change_observer_prototype import NickChangeObserverPrototype


class UserList(JoinObserverPrototype, KickObserverPrototype, LeaveObserverPrototype, NickChangeObserverPrototype):
    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def __init__(self):
        super().__init__()
        self.userList = {}

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_JOIN, ModuleType.ON_KICK, ModuleType.ON_LEAVE, ModuleType.ON_NICK_CHANGE]

    def update_on_kick(self, data: IRCData, connection: Connection):
        self._remove_user(data.nick, data.channel)

    def update_on_leave(self, data: IRCData, connection: Connection):
        self._remove_user(data.nick, data.channel)

    def update_on_join(self, data, connection):
        self.add_user(data)

    def update_on_nick_change(self, data: IRCData, connection: Connection):
        channel_userlist = self.userList[data.channel]
        user = self._remove_user(data.nick, data.channel)
        user.nick = data.message
        channel_userlist[user.nick] = user

    def clear_list(self):
        self.userList = {}

    def add_user(self, data: IRCData):
        user = RemoteUser(data.nick, data.user, data.host)
        self.update_user(user, data.channel)

    def update_user(self, user: RemoteUser, channel: str):
        channel_userlist = self._get_channel_userlist(channel)
        channel_userlist[user.nick] = user

    def get_user(self, channel: str, nick: str):
        users = self._get_channel_userlist(channel)
        if users is None:
            return None
        return users.get(nick, None)

    def _remove_user(self, nick: str, channel: str) -> Union[RemoteUser, None]:
        channel_userlist = self._get_channel_userlist(channel)
        if nick in channel_userlist:
            user = channel_userlist[nick]
            del channel_userlist[nick]
            return user
        return None

    def _get_channel_userlist(self, channel: str) -> dict:
        if channel not in self.userList:
            self.userList[channel] = {}
        return self.userList[channel]
