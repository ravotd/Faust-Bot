class StringBuffer:
    """

    """

    def __init__(self):
        """

        """
        self._buffer = str()

    def append(self, to_append):
        """

        :param to_append:
        :return:
        """
        self._buffer = self._buffer + to_append
        return self.get()

    def get(self):
        """

        :return:
        """
        ready = list()
        # Python do-while-loop
        idx = self._buffer.find('\n')
        while idx is not -1:
            data = self._buffer[0:idx]  #
            data = data.strip()
            if len(data) >= 1:
                ready.append(data)
            self._buffer = self._buffer[idx + 1:]
            idx = self._buffer.find('\n')
        return ready

    @property
    def buffer(self):
        """

        :return:
        """
        return self._buffer

    @buffer.setter
    def buffer(self, new_value):
        """

        :param new_value:
        :return:
        """
        self._buffer = new_value
