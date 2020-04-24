import random

from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from getraenkeOnlyGoodOnes import getraenke


class GiveDrinkToObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".givedrink"]

    @staticmethod
    def help():
        return ".givedrink NUTZER - schenkt jemand anders ein Getränke aus"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.givedrink') == -1:
            return
        receiver = data['message'].split()[1]
        if receiver == data['nick']:
            connection.send_back('Bitte nutze .drink um dir selbst ein Getränk zu besiorgen', data)
            return
        connection.send_back('\001ACTION serviert ' + receiver + ' ' + random.choice(getraenke) + '. Schöne Grüße von '+data['nick']+'\001', data)

