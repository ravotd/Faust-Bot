from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class ModmailObserver(PrivMsgObserverPrototype):
    def update_on_priv_msg(self, data):
        if data['message'].find('.modmail') == -1:
            return
        mods = Connection.singleton().details.get_mods()
        print(mods)
        message = data['message'].split('.modmail ')[1]
        for mod in mods:
            Connection.singleton().send_to_user(mod, data['nick'] + ' meldet: ' + message)
