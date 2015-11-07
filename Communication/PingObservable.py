class PingObservable(object):

    _observers = None
    _data = None

    def addObserver(self, observer):
        print(observer)
        if (self._observers == None):
            self._observers = {observer}
        else:
            self._observers = self._observers + observer

    def notifyObservers(self):
        for observer in self._observers:
            observer.update(self._data)

    def _input(self, data):
        self._data = data
        # hier kann noch gecheckt werden, ob data wirklich ein server ist, der ping haben will, oder sonstwas
        self.notifyObservers()

    def __init__(self):
        self._observers = None
        self._data = None