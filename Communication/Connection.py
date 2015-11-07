import socket
import re

from Communication.PingObservable import PingObservable
from Model import ConnectionDetails

class Connection(object):

    details = None
    irc = None
    ping = None

    def send(self):
        """
        Send to network
        :return:
        """

    def raw_send(self, message):
        self.irc.send(message.encode() + '\r\n'.encode())

    def receive(self):
        """
        receive from Network
        """
        data = self.irc.recv(4096).decode('UTF-8')
        data = data.rstrip()
        print(data)
        if data.find('PING') == 0:
            PingObservable._input(data.split()[1])
            return
        formatted_data = {}
        who = re.match('^:.*!', data)
        if who:
            who = who.group(0)
            who = who[1:-1]
        formatted_data['who'] = who
        where = re.search('PRIVMSG .* :', data)
        if where:
            where = where.group(0)
            where = where[8:-2]
            if who and where == details.get_nick():
                where = who
        formatted_data['where'] = where
        tmp = re.match('PRIVMSG .* :.*', data)
        if tmp:
            message = re.match(':.*', tmp.group(1))
            if message:
                message = message.group(0)
                message = message[1,-0]
        else:
            message = None
        formatted_data['message'] = message
        print(formatted_data)
        return formatted_data

    def establish(self):
        """
        establish the connection
        """
        global details
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.irc.connect((details.get_server(), details.get_port()))
        print(self.irc.recv(4096))
        self.irc.send("NICK ".encode() + details.get_nick().encode() + "\r\n".encode())
        self.irc.send("USER botty botty botty :IRC Bot\r\n".encode())
        self.irc.send("JOIN ".encode() + details.get_channel().encode() + '\r\n'.encode())

    def __init__(self, set_details: ConnectionDetails):
        global details
        details = set_details
        self._ping = PingObservable()

    def observePing(self, observer):
        """
        add observer to the observers of the ping-observable
        :param observer: observer to add
        """
        PingObservable.addObserver(self._ping, observer)
