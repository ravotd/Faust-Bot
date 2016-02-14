"""
mainfile, initializes everything
"""

# function declarations
from Communication.Connection import Connection
from Controler import ActivityObserver
from Controler import GoogleObserver
from Controler import PingAnswerObserver
from Controler import SeenObserver
from Controler import TitleObserver
from Controler import WikiObserver
from Controler import UserList
from Controler import Kicker
from Controler.CustomUserModules import ModmailObserver
from Model.ConnectionDetails import ConnectionDateils
import _thread


def setup():
    connection = Connection(ConnectionDateils(True))
    connection.establish()
    _thread.start_new_thread(connection.singleton().sender,())
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
    Connection.singleton().observePrivmsg(Activity )
    Connection.singleton().observePrivmsg(SeenObserver.SeenObserver())
    Connection.singleton().observePrivmsg(TitleObserver.TitleObserver())
    Connection.singleton().observePrivmsg(WikiObserver.WikiObserver())
    Connection.singleton().observePrivmsg(ModmailObserver.ModmailObserver())

def run():
    running = True
    while running:
        if Connection.singleton().receive() == False:
            return


def cleanup():
    pass


# starting of bot

def main():
    setup()
    run()
    cleanup()

main()
