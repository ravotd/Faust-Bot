class ConnectionDateils(object):
    def get_server(self):
        """
        :return: the server to connect to
        """
        return "irc.freenode.org"

    def get_nick(self):
        """
        :return: own nick
        """
        return "FaustBot74"

    def get_channel(self):
        """
        :return: the channel connected into
        """
        return "#faust-bot"

    def get_port(self):
        return 6667

    def get_lang(self):
        return "de-de"
