from FaustBot.Communication.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype
from enum import Enum
from datetime import datetime


class AntiSpamLevel(Enum):
    """
    Which action to be done if spam is detected.
    """
    OFF = 0
    WARN = 1
    WARN_KICK = 2
    KICK = 3
    WARN_KICK_BAN = 4
    KICK_BAN = 5


class AntiSpamAggressivity(Enum):
    """
    Settings to detect spam.
    a: Amount of seconds between two similiar messages to detect them as spam
    b: Amount of (non similiar) messages to be received with time-distance c, to detect them as spam
    c: Time between messages of b:
    d: Trustfactor
    """
    LOW = (3, 7, 0.5, 15)  # (a, b, c, d)
    MEDIUM = (5, 5, 0.7, 10)
    HIGH = (7, 3, 1.0, 5)
    ULTRA = (10, 3, 1.0, 2)


class AntiSpamEntry(object):
    """
    Entry collecting information about possible spammers.
    """

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
        self._anti_spam_aggressivity = AntiSpamAggressivity.LOW

    def update_on_priv_msg(self, data, connection: Connection):
        if self._anti_spam_level == AntiSpamLevel.OFF:
            return


    def is_spam(self, user: str, msg: str)
        pass 
