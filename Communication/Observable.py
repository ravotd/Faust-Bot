class Observable(object):

    _observers = []
    _data = []

    def addObserver(self, observer):
        self._observers.append(observer)

    def notifyObservers(self):
        for observer in self._observers:
            observer.update(self._data)

    def input(self, data):
        # here implement some data handling. Fill self._data with the data received
        raise NotImplementedError("Some Observable doesn't know what to do with its input data")


    def __init__(self):
        self._observers = []
        self._data = []
