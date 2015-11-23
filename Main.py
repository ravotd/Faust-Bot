"""
mainfile, initializes everything
"""

# function declarations
from Communication.Connection import Connection
from Controler import PingAnswerObserver
from Controler import ActivityObserver
from Model.ConnectionDetails import ConnectionDateils


def setup():
    connection = Connection(ConnectionDateils())
    connection.establish()

    Connection.singleton().observePing(PingAnswerObserver.ModulePing())
    Connection.singleton().observePrivmsg(ActivityObserver.AcitivityObserver())

def run():
    while True:
        Connection.singleton().receive()


def cleanup():
    pass


# starting of bot

def main():
    setup()
    run()
    cleanup()

main()
