from Communication.Observable import Observable


class PingObservable(Observable):

    def input(self, data):
        self._data = data
        # hier kann noch gecheckt werden, ob data wirklich ein server ist, der ping haben will, oder sonstwas
        # finde heraus, wer zurückgepingt werden muss, und ob das überhaupt ein ping-request ist oder ein user sich
        # einen spass erlaubt hat
        self._data = data
        self.notifyObservers()
        print(data)
