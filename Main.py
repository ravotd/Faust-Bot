"""
mainfile, initializes everything
"""

# function declarations
from Communication.Connection import Connection
from Controler import ModulePing
from Model.ConnectionDetails import ConnectionDateils


def setup():
    connection = Connection(ConnectionDateils())
    connection.establish()

    ping = ModulePing.ModulePing(connection)
    Connection.observePing(connection, ping)

    return connection


def run(connection: Connection):
    while True:
        data = connection.receive()


def cleanup():
    pass


# starting of bot

def main():
    connection = setup()
    run(connection)
    cleanup()

main()
