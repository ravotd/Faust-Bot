import socket
from Model import ConnectionDetails

class Connection(object):

    condets = None
    irc = None

    def send(self):
        """
        Send to network
        :return:
        """

    def receive(self):
        """
        receive from Network
        """
        data = self.irc.recv(4096)
        data = data.rstrip()
        print(data.decode(encoding='UTF-8'))



    def establish(self, dets: ConnectionDetails):
        """
        establish the connection
        """
        self.condets = dets
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.irc.connect((dets.get_server(), dets.get_port()))
        print(self.irc.recv(4096))
        self.irc.send("NICK ".encode() + dets.get_nick().encode() + "\r\n".encode())
        self.irc.send("USER botty botty botty :IRC Bot\r\n".encode())
        self.irc.send("JOIN ".encode() + dets.get_channel().encode() + '\r\n'.encode())

