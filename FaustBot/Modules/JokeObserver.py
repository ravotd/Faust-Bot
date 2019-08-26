import random
import time
from FaustBot.Communication import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype

jokes = [['Was ist grün und schaut durch das Schlüsselloch?','Ein Spionat']]


class JokeObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return [".joke"]

    @staticmethod
    def help():
        return ".joke erzählt einen Flachwitz"

    def update_on_priv_msg(self, data: dict, connection: Connection):
        if data['message'].find('.joke') == -1:
            return
        joke = random.choice(jokes)
        connection.send_back(joke[0], data)
        time.sleep(10)
        connection.send_back(joke[1], data)
