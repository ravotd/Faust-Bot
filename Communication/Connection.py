import socket
import re

from Communication.JoinObservable import JoinObservable
from Communication.PingObservable import PingObservable
from Communication.PrivmsgObservable import PrivmsgObservable
from Communication.LeaveObservable import LeaveObservable
from Communication.KickObservable import KickObservable
from Communication.NickChangeObservable import NickChangeObservable
from Model import ConnectionDetails
import queue
import time


class Connection(object):

    send_queue = queue.Queue()
    details = None
    irc = None
    instance = None

    def sender(self):
        while(True):
            self.irc.send(self.send_queue.get())
            time.sleep(1)

    @staticmethod
    def singleton():
        return Connection.instance;

    def send_channel(self, text):
        """
        Send to channel
        :return:
        """
        self.raw_send("PRIVMSG " + self.details.get_channel() + " :" + text[0:])

    def send_to_user(self, user, text):
        """
        Send to user
        :return:
        """
        self.raw_send('PRIVMSG ' + user + ' :' + text)

    def raw_send(self, message):
        self.send_queue.put(message.encode() + '\r\n'.encode())

    def receive(self):
        """
        receive from Network
        """
        error = False
        try:
            data = self.irc.recv(4096)
            self.data = data
            if len(data) == 0:
                return False
        except socket.timeout:
            return False
        data = data.decode('UTF-8', errors='replace')
        self.data = data
        data = data.rstrip()
        if data.find('PING') != -1:
            self._ping.input(data)
        if data.find('PRIVMSG') != -1:
            self._privmsg.input(data)
        if data.find(' JOIN ') != -1:
            self._join.input(data)
        if data.find(' PART ') != -1:
            self._leave.input(data)
        if data.find(' KICK ') != -1:
            self._kick.input(data)
        if data.find(' NICK ') != -1:
            self._nick.input(data)
        return True

    def last_data(self):
        return self.data

    def establish(self):
        """
        establish the connection
        """
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.irc.connect((self.details.get_server(), self.details.get_port()))
        print(self.irc.recv(4096))
        self.irc.send("NICK ".encode() + self.details.get_nick().encode() + "\r\n".encode())
        self.irc.send("USER botty botty botty :IRC Bot\r\n".encode())
        self.irc.send("JOIN ".encode() + self.details.get_channel().encode() + '\r\n'.encode())

    def __init__(self, set_details: ConnectionDetails):
        self.details = set_details
        self._ping = PingObservable()
        self._privmsg = PrivmsgObservable()
        self._join = JoinObservable()
        self._leave = LeaveObservable()
        self._kick = KickObservable()
        self._nick = NickChangeObservable()
        if Connection.instance != None:
            raise ReferenceError("Only one connection is supported, don't create a new one as long as one still exists!")
        Connection.instance = self

    def observePing(self, observer):
        """
        add observer to the observers of the ping-observable
        :param observer: observer to add
        """
        self._ping.addObserver(observer)

    def observePrivmsg(self, observer):
        """
        add observer to the observers of the ping-observable
        :param observer: observer to add
        """
        self._privmsg.addObserver(observer)

    def observeJoin(self, observer):
        self._join.addObserver(observer)

    def observeLeave(self, observer):
        self._leave.addObserver(observer)

    def observeKick(self, observer):
        self._kick.addObserver(observer)
