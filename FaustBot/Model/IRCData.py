class IRCData(object):

    def __init__(self, raw=''):
        self._channel = ''
        self._sender = ''
        self._nick = ''
        self._message = ''
        self._raw = raw
        if len(self._raw.strip()) is not 0:
            self.parse()

    def parse(self):
        pass

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
    # </editor-fold>
