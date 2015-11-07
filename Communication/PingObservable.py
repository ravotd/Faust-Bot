class PingObservable(object):

    _observers = None
    _data = None

    def addObserver(self, observer):
        global _observers
        print (observer)
        if (_observers != None):
            _observers = {observer}
        else:
            _observers = _observers + observer

    def notifyObservers(self):
        global _observers, _data
        for observer in _observers:
            observer.update(_data)

    def _input(self, data):
        global _data
        _data = data
        # hier kann noch gecheckt werden, ob data wirklich ein server ist, der ping haben will, oder sonstwas
        self.notifyObservers()

    def __init__(self):
        global _observers, _data
        _observers = None
        _data = None