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
    Connection.singleton().observe('join', userList)
    Connection.singleton().observe('join', Activity)
    Connection.singleton()._join.input_names(data)

    Connection.singleton().observe('kick', userList)
    Connection.singleton().observe('leave', userList)
    Connection.singleton().observe('nick', userList)
    Connection.singleton().observe('ping', PingAnswerObserver.ModulePing())
    Connection.singleton().observe('ping', Kicker.Kicker())
    Connection.singleton().observe('privmsg', Activity )
    Connection.singleton().observe('privmsg', SeenObserver.SeenObserver())
    Connection.singleton().observe('privmsg', TitleObserver.TitleObserver())
    Connection.singleton().observe('privmsg', WikiObserver.WikiObserver())
    Connection.singleton().observe('privmsg', ModmailObserver.ModmailObserver())

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
