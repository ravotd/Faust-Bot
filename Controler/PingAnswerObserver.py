from Communication.Connection import Connection
from Controler.PingObserverPrototype import PingObserverPrototype


class ModulePing(PingObserverPrototype):
    """
    A Class only reacting to pings
    """
    def update_on_ping(self, data):
        msg = 'PONG ' + data['server']
        Connection.singleton().raw_send(msg)

