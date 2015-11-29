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
            self.data[data.split(': ')[0]] = data.split(': ')[1].rstrip('\n').rstrip('\r')
            data = txt.readline()
        print(self.data)