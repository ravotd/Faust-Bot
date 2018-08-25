import _thread
import queue
import socket
import time
from threading import Condition

from faustbot.communication.join_observable import JoinObservable
from faustbot.communication.kick_observable import KickObservable
from faustbot.communication.leave_observable import LeaveObservable
from faustbot.communication.magic_number_observable import MagicNumberObservable
from faustbot.communication.nick_change_observable import NickChangeObservable
from faustbot.communication.notice_observable import NoticeObservable
from faustbot.communication.ping_observable import PingObservable
from faustbot.communication.privmsg_observable import PrivmsgObservable
from faustbot.model.config import Config
from faustbot.model.irc_data import IRCData
from faustbot.util import logging
from faustbot.util.buffer import StringBuffer


class Connection(object):
    def _send_queue_worker(self):
        while True:
            msg = self.send_queue.get()
            if msg[-1] is not b'\n':
                msg = msg + b'\n'
            self._irc.send(msg)
            time.sleep(1)

    def channel_privmsg(self, message: str, channel: str):
        """
        Send to channel
        :return:
        """
        self.raw_send('PRIVMSG %s :%s' % (channel, message))

    def user_privmsg(self, message: str, user: str):
        """
        Send to user
        :return:
        """
        self.raw_send('PRIVMSG %s :%s ' % (user, message))

    def send_back(self, message: str, received: IRCData):
        """
        Send message to the channel the command got received in
        :param received:
        :param message:
        :return:
        """
        if received.is_query():
            self.user_privmsg(message, received.nick)
        else:
            self.channel_privmsg(message, received.channel)

    def raw_send(self, message):
        self.send_queue.put(message.encode() + '\r\n'.encode())

    def receive(self) -> bool:
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
        self._logger.debug('received: ' + data)
        data_lines = self._receiver_buffer.append(data)
        if data is None:
            return False
        self._notify(data_lines)
        return True

    def _notify(self, data_lines: iter):
        for data in data_lines:
            data = data.strip()
            self.data = IRCData(data)
            self._logger.debug('Received message from %s in channel %s: %s' % (self.data.nick, self.data.channel,
                                                                               self.data.message))
            if self.data.command == 'PING':
                self.ping_observable.input(self.data, self)
            elif self.data.command == 'JOIN':
                self.join_observable.input(self.data, self)
            elif self.data.command == 'PART' or self.data.command == 'QUIT':
                self.leave_observable.input(self.data, self)
            elif self.data.command == 'KICK':
                self.kick_observable.input(self.data, self)
            elif self.data.command == 'NICK':
                self.nick_change_observable.input(self.data, self)
            elif self.data.command == 'NOTICE':
                self.notice_observable.input(self.data, self)
            elif self.data.command == 'PRIVMSG':
                self.priv_msg_observable.input(self.data, self)
            else:
                try:
                    int(self.data.command)
                    self.magic_number_observable.input(self.data, self)
                except Exception as e:
                    self._logger.error(e)

    def _send_unbuffered(self, message: str):
        self._irc.send(message.encode())

    def is_identified(self, user: str) -> bool:
        self.user_privmsg('NickServ', 'ACC ' + user)
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
        self._logger.info(self._irc.recv(512))
        self._send_unbuffered("NICK %s \r\n" % self.config.nick)
        self._send_unbuffered("USER botty botty botty :IRC Bot\r\n")
        for c in self.config.channel:
            name = c.name
            self._send_unbuffered("JOIN %s \r\n" % name)
            self._send_unbuffered("WHO %s \r\n" % name)
        _thread.start_new_thread(self._send_queue_worker, ())

    def __init__(self, configuration: Config):
        self._logger = logging.get_logger(Connection.__name__)
        self._irc = None
        self.config = configuration
        self.send_queue = queue.Queue()
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
