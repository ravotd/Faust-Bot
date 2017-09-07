class StringBuffer:
    def __init__(self):
        self._buffer = str()

    def append(self, to_append):
        self._buffer = self._buffer + to_append
        return self.get()

    def get(self):
        idx = self._buffer.find('\n')
        if idx is not -1:
            ready = self._buffer[0:idx]
            self._buffer = self._buffer[idx + 1:]
            return ready
        return None

    @property
    def buffer(self):
        return self._buffer

    @buffer.getter
    def set_buffer(self, new_value):
        self._buffer = new_value
