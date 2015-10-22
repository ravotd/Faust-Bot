"""
mainfile, initializes everything
"""

# function declarations
from Communication import Connection
from Model import ConnectionDetails

conn = None

def setup():
    dets = ConnectionDetails.ConnectionDateils()
    conn = Connection.Connection()
    conn.establish(dets)

def run():
    while True:
        data = conn.receive()

def cleanup():
    pass


# starting of bot

setup()

run()

cleanup()