from random import randint
from typing import Tuple, List

from faustbot.communication.connection import Connection
from faustbot.model.irc_data import IRCData
from faustbot.modules.module_type import ModuleType
from faustbot.modules.prototypes.ping_observer_prototype import PingObserverPrototype
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class DuckObserver(PrivMsgObserverPrototype, PingObserverPrototype):
    BEFRIEND = '.freunde'
    SHOOT = '.schiessen'
    START_HUNT = '.starthunt'
    STOP_HUNT = '.stophunt'

    @staticmethod
    def cmd() -> List[str]:
        return [DuckObserver.BEFRIEND, DuckObserver.SHOOT, DuckObserver.START_HUNT, DuckObserver.STOP_HUNT]

    @staticmethod
    def help() -> str:
        return 'duck game'

    @staticmethod
    def get_module_types() -> List[ModuleType]:
        return [ModuleType.ON_MSG, ModuleType.ON_PING]

    def __init__(self):
        super().__init__()
        self.hunts = {}

    def update_on_priv_msg(self, data, connection: Connection) -> None:
        if data.is_query():
            connection.send_back("channel command", data)
        if data.message.find(DuckObserver.START_HUNT) != -1:
            self.start_hunt(data, connection)
        elif data.message.find(DuckObserver.STOP_HUNT) != -1:
            self.stop_hunt(data, connection)
        elif data.message.find(DuckObserver.BEFRIEND) != -1:
            self.befriend(data, connection)
        elif data.message.find(DuckObserver.SHOOT) != -1:
            self.shoot(data, connection)

    def start_hunt(self, data, connection) -> bool:
        if not self._is_idented_mod(data, connection):
            msg = "Dir fehlen leider die Rechte zum Starte der Jagd, %s." % data.nick
            connection.send_back(msg, data)
            return False
        if data.channel not in self.hunts:
            self.hunts[data.channel] = {'alive': 0, 'highscore': {}}
            connection.send_back("Jagd eröffnet", data)
        return True

    def stop_hunt(self, data, connection) -> bool:
        if not self._is_idented_mod(data, connection):
            msg = "Dir fehlen leider die Rechte zum Stoppen der Jagd, %s." % data.nick
            connection.send_back(msg, data)
            return False
        if data.channel in self.hunts:
            del self.hunts[data.channel]
            connection.send_back("Jagd beendet", data)
        return True

    def befriend(self, data: IRCData, connection) -> bool:
        if not self.is_game_running(data.channel):
            connection.send_back("Es läuft derzeit keine Entenjagd.", data)
            return False
        channel_data, alive, highscore = self.get_channel_data(data.channel)
        if alive > 0:
            channel_data['alive'] -= 1
            DuckObserver.increase_befriend(highscore, data.nick)
            DuckObserver.send_user_stats(highscore, data, connection)
        else:
            msg = "%s probiert eine nicht existente Ente zu befreunden" % data.nick
            connection.send_back(msg, data)
        return True

    def shoot(self, data: IRCData, connection) -> bool:
        if not self.is_game_running(data.channel):
            connection.send_back("Es läuft derzeit keine Entenjagd.", data)
            return False
        channel_data, alive, highscore = self.get_channel_data(data.channel)
        if alive > 0:
            channel_data['alive'] -= 1
            DuckObserver.increase_killed(highscore, data.nick)
            DuckObserver.send_user_stats(highscore, data, connection)
        else:
            msg = "%s schießt ins Nichts" % data.nick
            connection.send_back(msg, data)
        return True

    def update_on_ping(self, data, connection: Connection) -> None:
        for channel, channel_data in self.hunts.items():
            if 1 == randint(1, 11):
                if channel_data['alive'] == 0:
                    connection.channel_privmsg("*. *. *. *  <<( W °)>  *. *. * Quack!", channel)
                    channel_data['alive'] = 1

    def _is_idented_mod(self, data: IRCData, connection: Connection) -> bool:
        return data.nick in self._config.channels[data.channel].mods and connection.is_identified(data.nick)

    def is_game_running(self, channel: str) -> bool:
        return channel in self.hunts

    def get_channel_data(self, channel: str) -> Tuple[dict, int, dict]:
        return self.hunts[channel], self.hunts[channel]['alive'], self.hunts[channel]['highscore']

    @staticmethod
    def get_user_highscore(highscore: dict, nick: str) -> Tuple[int, int]:
        return highscore[nick]['befriend'], highscore[nick]['killed']

    @staticmethod
    def send_user_stats(highscore: dict, data: IRCData, connection: Connection) -> None:
        befriend, killed = DuckObserver.get_user_highscore(highscore, data.nick)
        msg = "{} hat schon {} befreundete und {} getötete Enten.".format(data.nick, befriend, killed)
        connection.send_back(msg, data)

    @staticmethod
    def check_highscore_existence(highscore: dict, nick: str) -> None:
        if nick not in highscore:
            highscore[nick] = {'befriend': 0, 'killed': 0}

    @staticmethod
    def increase_befriend(highscore: dict, nick: str) -> None:
        DuckObserver.check_highscore_existence(highscore, nick)
        highscore[nick]['befriend'] += 1

    @staticmethod
    def increase_killed(highscore: dict, nick: str) -> None:
        DuckObserver.check_highscore_existence(highscore, nick)
        highscore[nick]['killed'] += 1
