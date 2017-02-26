import _thread
import queue
import socket
import time

from FaustBot.Communication.JoinObservable import JoinObservable
from FaustBot.Communication.KickObservable import KickObservable
from FaustBot.Communication.LeaveObservable import LeaveObservable
from FaustBot.Communication.NickChangeObservable import NickChangeObservable
from FaustBot.Communication.PingObservable import PingObservable
from FaustBot.Communication.PrivmsgObservable import PrivmsgObservable
from FaustBot.Model.ConnectionDetails import ConnectionDetails


class Connection(object):
    send_queue = queue.Queue()
    details = None
    irc = None
    instance = None

    def sender(self):
        while True:
            self.irc.send(self.send_queue.get())
            time.sleep(1)

    @staticmethod
    def singleton():
        return Connection.instance

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

    def send_back(self, text, data):
        """
        Send message to the channel the command got received in
        :param message:
        :param data: needed because of concurrency, there can't be a global variable holding where messages came from
        :return:
        """
        if data['channel'] == self.details.get_nick():
            self.send_to_user(data['nick'], text)
        else:
            self.send_channel(text)

    def raw_send(self, message):
        self.send_queue.put(message.encode() + '\r\n'.encode())

    def receive(self):
        """
        receive from Network
        """
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
            self.ping_observable.input(data)
        if data.find('PRIVMSG') != -1:
            self.priv_msg_observable.input(data)
        if data.find(' JOIN ') != -1:
            self.join_observable.input(data)
        if data.find(' PART ') != -1 or data.find(' QUIT ') != -1:
            self.leave_observable.input(data)
        if data.find(' KICK ') != -1:
            self.kick_observable.input(data)
        if data.find(' NICK ') != -1:
            self.nick_change_observable.input(data)
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
        _thread.start_new_thread(self.sender, ())

    def __init__(self, set_details: ConnectionDetails):
        self.details = set_details
        self.ping_observable = PingObservable()
        self.priv_msg_observable = PrivmsgObservable()
        self.join_observable = JoinObservable()
        self.leave_observable = LeaveObservable()
        self.kick_observable = KickObservable()
        self.nick_change_observable = NickChangeObservable()
        self.data = None
        if Connection.instance is not None:
            raise ReferenceError(
                "Only one connection is supported, don't create a new one as long as one still exists!")
        Connection.instance = self


