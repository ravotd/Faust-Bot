import _thread

from Communication.Observable import Observable

class LeaveObservable(Observable):

    def input(self, raw_data):
        data = {}
        leaveOrPart = "PART"  if raw_data.find('PART') != -1 else "QUIT"
        data['raw'] = raw_data
        data['nick'] = raw_data.split('!')[0][1:]
        data['channel'] = raw_data.split(leaveOrPart+' ')[1].split(' :')[0]
        data['raw_nick'] = raw_data.split(' '+leaveOrPart)[0][1:]
        self.notifyObservers(data)

    def notifyObservers(self, data):
         for observer in self._observers:
            _thread.start_new_thread(observer.__class__.update_on_leave, (observer, data))
