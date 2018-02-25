from FaustBot.Communication.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype
from enum import Enum
from datetime import datetime

class AntiSpamLevel(Enum):
    OFF = 0
    WARN = 1
    WARN_KICK = 2
    KICK = 3
    WARN_KICK_BAN = 4
    KICK_BAN = 5


class AntiSpamAggressivity(Enum):
    LOW = 3
    MEDIUM = 5
    HIGH = 7
    ULTRA = 10


class AntiSpamEntry(object):
    def __init__():
        super().__init__()
        self.user = ""
        self.warn_count = 0
        self.msg = ""
        self.timestamp = datetime.now() 

    @property
    def user(self):
        return self.user

    @user.setter
    def user(self, user)
        self.user = user
    
    @property
    def warn_count(self):
        return self.warn_count

    @warn_count.setter
    def warn_count(self, warn_count)
        self.warn_count = warn_count

    def inc_warn_count(self)
        self.warn_count += 1

    @property
    def msg(self):
        return self.msg

    @msg.setter
    def msg(self, msg):
        self.msg = msg

    @property
    def timestamp(self):
        return self.timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self.timestamp = timestamp


class AntiSpamObserver(PrivMsgObserverPrototype):

    @staticmethod
    def cmd():
        raise NotImplementedError("TBD!")

    @staticmethod
    def help():
        raise NotImplementedError("TBD!")

    def __init__(self):
        super().__init__()
        self._msg_map = dict()
        self._anti_spam_level = AntiSpamLevel.OFF

    def update_on_priv_msg(self, data, connection: Connection):
        if self._anti_spam_level == AntiSpamLevel.OFF:
            return


    def is_spam(self, user: str, msg: str)
        pass 
