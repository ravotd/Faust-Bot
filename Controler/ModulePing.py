from Communication.Connection import Connection


class ModulePing(object):
    """
    A Class only reacting to pings
    """
    def update(self, data):
        msg = 'PONG ' + data['server']
        self.connection.raw_send(msg)

    def __init__(self, source):
        self.connection = source
