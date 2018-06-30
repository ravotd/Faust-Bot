class IRCData(object):

    def __init__(self, raw=''):
        self._channel = ''
        self._sender = ''
        self._nick = ''
        self._message = ''
        self._user = ''
        self._host = ''
        self._raw = raw
        self._command = ''
        if len(self._raw.strip()) is not 0:
            self.parse()

    def parse(self, raw: str = None):
        if raw is not None:
            self._raw = raw
        prefix, self._command, self._channel, *self._message = self._raw.split(' ', maxsplit=3)
        if len(self._message) is 0:
            self._message = ''
        else:
            self._message = self._message[0]
        host_mask = prefix.lstrip(':')
        if '!' in prefix:
            self._nick, user_host = host_mask.split('!')
            self._user, self._host = user_host.split('@')
        else:
            self._nick = host_mask

    # <editor-fold desc=Properties>
    @property
    def channel(self) -> str:
        return self._channel

    @channel.setter
    def channel(self, value: str):
        self._channel = value

    @property
    def sender(self) -> str:
        return self._sender

    @sender.setter
    def sender(self, value: str):
        self._sender = value

    @property
    def raw(self) -> str:
        return self._raw

    @raw.setter
    def raw(self, value: str):
        self._raw = value

    @property
    def nick(self) -> str:
        return self._nick

    @nick.setter
    def nick(self, value: str):
        self._nick = value

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, value: str):
        self._message = value

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, value: str):
        self._user = value

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def command(self) -> str:
        return self._command

    @command.setter
    def command(self, value: str):
        self._command = value
    # </editor-fold>
