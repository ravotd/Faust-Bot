# from ..faustbot import ModuleType
from faustbot.communication.connection import Connection
from faustbot.model.irc_data import IRCData
from faustbot.model.user_provider import UserProvider
from faustbot.modules.module_type import ModuleType
from faustbot.modules.prototypes.join_observer_prototype import JoinObserverPrototype
from faustbot.modules.prototypes.nick_change_observer_prototype import NickChangeObserverPrototype
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class ActivityObserver(PrivMsgObserverPrototype, JoinObserverPrototype, NickChangeObserverPrototype):
    """
    A Class only reacting to pings
    """

    @staticmethod
    def cmd():
        return None

    @staticmethod
    def help():
        return None

    def update_on_join(self, data: IRCData, connection: Connection):
        users = UserProvider()
        channel = connection.config.get_channel_by_name(data.channel)
        if channel is not None:
            users.set_active(data.nick, data.channel)

    def update_on_priv_msg(self, data: IRCData, connection: Connection):
        users = UserProvider()
        channel = connection.config.get_channel_by_name(data.channel)
        if channel is not None:
            users.set_active(data.nick, data.channel)
            users.add_characters(data.nick, len(data.message), data.channel)

    def update_on_nick_change(self, data, connection: Connection):
        users = UserProvider()
        users.set_active(data.nick, data.channel)

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_MSG, ModuleType.ON_JOIN, ModuleType.ON_NICK_CHANGE]
