from Communication import Connection


class ModulePing(object):
    """
    A Class only reacting to pings
    """
    def update(self, data):
        msg = "PONG " + data['server']
        Connection.raw_send(msg)
        print (msg + 'ping sent via observable')

    def __init__(self):
        pass
