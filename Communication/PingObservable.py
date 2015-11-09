from Communication.Observable import Observable


class PingObservable(Observable):

    def input(self, rawline):

        #TODO: Please split the data in data['raw'] data['source'] 
        self.notifyObservers(data)
        print(data)
