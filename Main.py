"""
mainfile, initializes everything
"""

# function declarations
from Communication.Connection import Connection
from Controler import PingAnswerObserver
from Model.ConnectionDetails import ConnectionDateils


def setup():
    Connection.singleton().establish()

    Connection.singleton().observePing(PingAnswerObserver.ModulePing())

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
