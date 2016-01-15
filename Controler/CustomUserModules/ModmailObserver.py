from Communication.Connection import Connection
from Controler.PrivMsgObserverPrototype import PrivMsgObserverPrototype

class ModmailObserver(PrivMsgObserverPrototype):


    def update_on_priv_msg(self, data):
        mods = {'nick1', 'nick2'}
        if data['message'].find('.modmail') == -1:
            return
        message = data['message'].split('.modmail ')[1]
        for mod in mods:
            Connection.singleton().send_to_user(mod, data['nick'] + ' meldet: ' + message)
