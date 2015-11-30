"""
mainfile, initializes everything
"""

# function declarations
from Communication.Connection import Connection
from Controler import PingAnswerObserver
from Controler import ActivityObserver
from Controler import SeenObserver
from Model.ConnectionDetails import ConnectionDateils


def setup():
    connection = Connection(ConnectionDateils(True))
    connection.establish()
    # bind names-module
    # while names-module wasn't called yet
    #     receive()
    Connection.singleton().receive()
    while Connection.singleton().last_data().split(' ')[1] != '353':
        Connection.singleton().receive()

    Connection.singleton().observePing(PingAnswerObserver.ModulePing())
    Connection.singleton().observePrivmsg(ActivityObserver.AcitivityObserver())
    Connection.singleton().observePrivmsg(SeenObserver.SeenObserver())

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
