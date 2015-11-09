from Communication import Connection


class ModulePing(object):
    """
    A Class only reacting to pings
    """
    def update(self, data):
        print('im module!!!!!!')
        msg = "PONG " + data['server']
        print('msg: ' + msg)
        Connection.raw_send(msg)
        print(msg + 'ping sent via observable')

    def __init__(self):
        pass
