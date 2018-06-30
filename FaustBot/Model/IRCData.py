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
        self._special_command = False
        if len(self._raw.strip()) is not 0:
            self.parse()

    def parse(self, raw: str = None):
        if raw is not None:
            self.raw = raw
        if self.raw.split(' ')[0].isupper():
            self._parse_non_directed()
            return
        self.special_command = False
        prefix, self.command, self.channel, *self.message = self._raw.split(' ', maxsplit=3)
        if len(self.message) is 0:
            self.message = ''
        else:
            self.message = self.message[0]
        host_mask = prefix.lstrip(':')
        if '!' in prefix:
            self.nick, user_host = host_mask.split('!')
            self.user, self.host = user_host.split('@')
        else:
            self.nick = host_mask

    def _parse_non_directed(self):
        self.special_command = True
        self.command, *rest = self.raw.split(' ', maxsplit=2)
        if len(rest) <= 2:
            self.nick = rest[0].lstrip(':')
        if len(rest) == 2:
            self.channel = rest[1].lstrip(':')
        if len(rest) > 2:
            self.message = rest[2]

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

    @property
    def special_command(self) -> bool:
        return self._special_command

    @special_command.setter
    def special_command(self, value: bool):
        self._special_command = value
    # </editor-fold>
