from faustbot.model.irc_data import IRCData


class Observable(object):
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)
        print("appended(" + str(observer.__class__) + ")")

    def get_observer(self):
        return self._observers

    # data has to be a dictionary matching the structure of the query
    def notify_observers(self, data: IRCData, connection):
        # here implement some data handling. Fill self._data with the data received
        raise NotImplementedError("Some Observable doesn't know what to do with its input data")

    def input(self, data: IRCData, connection):
        # here implement some data handling. Fill self._data with the data received
        self.notify_observers(data, connection)

    def rm_observer(self, observer):
        self._observers.remove(observer)
