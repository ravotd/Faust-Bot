from Communication.Observable import Observable


class PingObservable(Observable):

    def input(self, raw_data):
        data = {}
        data['raw'] = raw_data
        if (raw_data.find('PING') == 0):
            data['server'] = raw_data.split('PING ')[1]
        # hier kann noch gecheckt werden, ob data wirklich ein server ist, der ping haben will, oder sonstwas
        # finde heraus, wer zurückgepingt werden muss, und ob das überhaupt ein ping-request ist oder ein user sich
        # einen spass erlaubt hat
        self.notifyObservers(data)
