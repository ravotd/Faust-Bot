"""
mainfile, initializes everything
"""

# function declarations
import _thread

from Communication.Connection import Connection
from Controler import ActivityObserver
from Controler import Kicker
from Controler import PingAnswerObserver
from Controler import SeenObserver
from Controler import TitleObserver
from Controler import UserList
from Controler import WikiObserver
from Controler.CustomUserModules import ICDObserver
from Controler.CustomUserModules import ModmailObserver
from Model.ConnectionDetails import ConnectionDateils


def setup():
    connection = Connection(ConnectionDateils(True))
    connection.establish()
    _thread.start_new_thread(connection.singleton().sender, ())
    userList = UserList.UserList()
    Activity = ActivityObserver.AcitivityObserver()
    Connection.singleton().receive()
    data = Connection.singleton().last_data()
    while -1 == data.find('353'):
        Connection.singleton().receive()
        data = Connection.singleton().last_data()
    Connection.singleton().observeJoin(userList)
    Connection.singleton().observeJoin(Activity)
    Connection.singleton()._join.input_names(data)

    Connection.singleton().observeKick(userList)
    Connection.singleton().observeLeave(userList)
    Connection.singleton().observeNickChange(userList)
    Connection.singleton().observeNickChange(Activity)
    Connection.singleton().observePing(PingAnswerObserver.ModulePing())
    Connection.singleton().observePing(Kicker.Kicker())
    Connection.singleton().observePrivmsg(Activity)
    Connection.singleton().observePrivmsg(SeenObserver.SeenObserver())
    Connection.singleton().observePrivmsg(TitleObserver.TitleObserver())
    Connection.singleton().observePrivmsg(WikiObserver.WikiObserver())
    Connection.singleton().observePrivmsg(ModmailObserver.ModmailObserver())
    Connection.singleton().observePrivmsg(ICDObserver.ICDObserver())


def run():
    running = True
    while running:
        if not Connection.singleton().receive():
            return


def cleanup():
    pass


# starting of bot

def main():
    setup()
    run()
    cleanup()


main()
