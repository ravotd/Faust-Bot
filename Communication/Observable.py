class Observable(object):
    
    def __init__(self):
        self._observers = []

    def addObserver(self, observer):
        self._observers.append(observer)
    
    #data has to be a dictionary matching the structure of the query
    def notifyObservers(self, data):
        for observer in self._observers:
            observer.update(data)

    def input(self, raw_data):
        # here implement some data handling. Fill self._data with the data received
        raise NotImplementedError("Some Observable doesn't know what to do with its input data")
