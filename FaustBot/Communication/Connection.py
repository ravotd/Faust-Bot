import _thread
import queue
import socket
import time
from threading import Condition

from FaustBot.Communication.JoinObservable import JoinObservable
from FaustBot.Communication.KickObservable import KickObservable
from FaustBot.Communication.LeaveObservable import LeaveObservable
from FaustBot.Communication.MagicNumberObservable import MagicNumberObservable
from FaustBot.Communication.NickChangeObservable import NickChangeObservable
from FaustBot.Communication.NoticeObservable import NoticeObservable
from FaustBot.Communication.PingObservable import PingObservable
from FaustBot.Communication.PrivmsgObservable import PrivmsgObservable
from FaustBot.Model.Config import Config
from FaustBot.StringBuffer import StringBuffer


class Connection(object):
    send_queue = queue.Queue()
    config = None
    _irc = None

    def sender(self):
        while True:
            msg = self.send_queue.get()
            if msg[-1] is not b'\n':
                msg = msg + b'\n'
            self._irc.send(msg)
            time.sleep(1)

    def send_channel(self, text):
        """
        Send to channel
        :return:
        """
        self.raw_send("PRIVMSG " + self.config.get_channel() + " :" + text[0:])

    def send_to_user(self, user, text):
        """
        Send to user
        :return:
        """
        self.raw_send('PRIVMSG ' + user + ' :' + text)

    def send_back(self, text, data):
        """
        Send message to the channel the command got received in
        :param text:
        :param data: needed because of concurrency, there can't be a global variable holding where messages came from
        :return:
        """
        if data['channel'] == self.config.get_nick():
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
            data = self._irc.recv(4096)
            if len(data) == 0:
                return False
        except socket.timeout:
            return False
        data = data.decode('UTF-8', errors='replace')
        # print('received: \n' + data)
        data_lines = self._receiver_buffer.append(data)
        if data is None:
            return False
        # print('split: ')
        for data in data_lines:
            # print(data)
            data = data.rstrip()
            self.data = data

            split = data.split(' ')
            if not len(split) >= 2:
                continue
            command = split[1]
            #         print(command)
            if data.split(' ')[0] == 'PING':
                self.ping_observable.input(data, self)
            elif command == 'JOIN':
                self.join_observable.input(data, self)
            elif command == 'PART' or command == 'QUIT':
                self.leave_observable.input(data, self)
            elif command == 'KICK':
                self.kick_observable.input(data, self)
            elif command == 'NICK':
                self.nick_change_observable.input(data, self)
            elif command == 'NOTICE':
                self.notice_observable.input(data, self)
            elif command == 'PRIVMSG':
                self.priv_msg_observable.input(data, self)
            else:
                try:
                    int(command)
                    self.magic_number_observable.input(data, self)
                except Exception:
                    pass

        return True

    def _notify(self):
        pass

    def is_identified(self, user: str):
        self.send_to_user('NickServ', 'ACC ' + user)
        with self.condition_lock:
            while user not in self.idented_look_up:
                self.condition_lock.wait()
            is_identified = self.idented_look_up[user]
            del self.idented_look_up[user]
            return is_identified

    def last_data(self):
        return self.data

    def establish(self):
        """
        establish the connection
        """
        self._irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._irc.connect((self.config.server, self.config.port))
        print(self._irc.recv(512))
        self._irc.send("NICK %s \r\n" % self.config.nick())
        self._irc.send("USER botty botty botty :IRC Bot\r\n")
        for c in self.config.channel:
            name = c.name
            self._irc.send("JOIN %s \r\n" % name)
            self._irc.send("WHO %s \r\n" % name)
        _thread.start_new_thread(self.sender, ())

    def __init__(self, configuration: Config):
        self.config = configuration
        self.ping_observable = PingObservable()
        self.priv_msg_observable = PrivmsgObservable()
        self.join_observable = JoinObservable()
        self.leave_observable = LeaveObservable()
        self.kick_observable = KickObservable()
        self.nick_change_observable = NickChangeObservable()
        self.notice_observable = NoticeObservable()
        self.magic_number_observable = MagicNumberObservable()
        self.condition_lock = Condition()
        self.idented_look_up = {}
        self.data = None
        self._receiver_buffer = StringBuffer()
