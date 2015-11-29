class ConnectionDateils(object):

    def get_server(self):
        """
        :return: the server to connect to
        """
        return self.data['server']

    def get_nick(self):
        """
        :return: own nick
        """
        return self.data['nick']

    def get_channel(self):
        """
        :return: the channel connected into
        """
        return self.data['channel']

    def get_port(self):
        return int(self.data['port'])

    def get_lang(self):
        return self.data['lang']

    def change_lang(self, lang):
        self.data['lang'] = lang

    def __init__(self):
        txt = open('config.txt')
        self.data = {}
        data = txt.readline()
        while (data != ''):
            # TODO ERROR next line won't work with /r/n as line end in config file! that has to be fixed before release!
            self.data[data.split(': ')[0]] = data.split(': ')[1][0:-1]
            data = txt.readline()
        print(self.data)