from collections import defaultdict
from random import randint

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.ModuleType import ModuleType
from FaustBot.Modules.PingObserverPrototype import PingObserverPrototype
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class DuckObserver(PrivMsgObserverPrototype, PingObserverPrototype):
    @staticmethod
    def cmd():
        return ['.freunde', '.schiessen', '.starthunt','.stophunt']

    @staticmethod
    def help():
        return 'duck game'

    @staticmethod
    def get_module_types():
        return [ModuleType.ON_MSG, ModuleType.ON_PING]

    def __init__(self):
        super().__init__()
        self.active = 0
        self.duck_alive = 0
        self.ducks_hunt = defaultdict(int)
        self.ducks_befriend = defaultdict(int)

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.starthunt') != -1:
            if not self._is_idented_mod(data, connection):
                connection.send_back("Dir fehlen leider die Rechte zum Starten der Jagd, " + data['nick'] + ".",data)
                return
            self.active = 1
            connection.send_channel("Jagd eröffnet")
            return
        if data['message'].find('.stophunt') != -1:
            if not self._is_idented_mod(data, connection):
                connection.send_back("Dir fehlen leider die Rechte zum Stoppen der Jagd, " + data['nick'] + ".",
                                     data)
                return
            self.active = 0
            self.duck_alive = 0
            connection.send_channel("Jagd beended")
            return
        if data['message'].find('.freunde') != -1:
            self.befriend(data, connection)
        if data['message'].find('.schiessen') != -1:
            self.shoot(data, connection)

    def befriend(self, data, connection):
        if self.duck_alive == 1:
            self.duck_alive = 0
            self.ducks_befriend[data['nick']] += 1
            connection.send_channel(data['nick'] + " hat schon " + str(self.ducks_befriend[data['nick']]) + " befreundete Enten und " + str(self.ducks_hunt[data['nick']]) + " getötete Enten.")
            return
        if (self.duck_alive == 0 and self.active == 1):
            connection.send_channel(data['nick']+ " probiert eine nicht existente Ente zu befreunden")
        if self.active == 0:
            connection.send_channel("Es läuft derzeit keine Entenjagd.")

    def shoot(self, data, connection):
        if self.duck_alive == 1:
            self.duck_alive = 0
            self.ducks_hunt[data['nick']] += 1
            connection.send_channel(data['nick'] + " hat schon " + str(self.ducks_befriend[data['nick']]) + " befreundete Enten und " + str(self.ducks_hunt[data['nick']]) + " getötete Enten.")
            return
        if (self.duck_alive == 0 and self.active == 1):
            connection.send_channel(data['nick']+ " schiesst ins Nichts")
        if self.active == 0:
            connection.send_channel("Es läuft derzeit keine Entenjagd.")

    def update_on_ping(self, data, connection: Connection):
        if self.active == 0:
            return
        if 1 == randint(1,11):
            if self.duck_alive == 0:
                connection.send_channel("*. *. *. * <<w°)> *. *. * Quack!")
                self.duck_alive = 1

    def _is_idented_mod(self, data: dict, connection: Connection):
        return data['nick'] in self._config.mods and connection.is_identified(data['nick'])
