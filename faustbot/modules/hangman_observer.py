from typing import List

from faustbot.communication.connection import Connection
from faustbot.model.irc_data import IRCData
from faustbot.modules.prototypes.privmsg_observer_prototype import PrivMsgObserverPrototype


class Word(object):
    def __init__(self, word):
        self.tries_left = 11
        self.word = word
        self.guessed = ['-', '/', ' ', '_']


class HangmanObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd() -> List[str]:
        return ['.guess', '.word', '.stop']

    @staticmethod
    def help() -> str:
        return 'hangman game'

    def __init__(self):
        super().__init__()
        self.words = {}

    def update_on_priv_msg(self, data: IRCData, connection: Connection) -> None:
        if data.message.find('.guess ') != -1:
            self.guess(data, connection)
            return
        elif data.message.find('.word ') != -1:
            self.enter_new_word(data, connection)
        elif data.message.find('.stop') != -1:
            self.stop_game(data, connection)

    def stop_game(self, data: IRCData, connection: Connection) -> None:
        if data.channel in self.words:
            word = self.words[data.channel]
            connection.send_back("Spiel gestoppt das Wort war: %s" % word.word, data)
            del self.words[data.channel]

    def guess(self, data: IRCData, connection: Connection) -> None:
        if data.is_query():
            connection.send_back("Sorry, das Spiel läuft nur im Channel", data)
            return
        word = self.words.get(data.channel)
        current_try = data.message.split(' ')[1].upper()
        if word is None:
            connection.send_back("Flüstere mir ein neues Wort mit .word %s DEIN-WORT" % data.channel, data)
            return
        elif current_try == word.word:
            connection.send_back("Korrekt: " + current_try, data)
            del self.words[data.channel]
        elif current_try in word.word:
            word.guessed += current_try
            self.send_stats(data.channel, connection)
        else:
            word.tries_left -= 1
            self.send_stats(data.channel, connection)

    def enter_new_word(self, data, connection) -> None:
        cmd, channel, new_word, *ign = data.message.split(' ', maxsplit=3)
        if channel not in self.words:
            word = Word(new_word)
            self.words[channel] = word
            connection.send_back("Danke für das Wort, es ist nun im Spiel!", data)
            self.send_stats(channel, connection)
        else:
            connection.send_back("Sorry es läuft bereits ein Wort", data)

    def send_stats(self, channel: str, connection: Connection) -> None:
        word_out = ""
        failedChars = 0
        word = self.words[channel]
        for char in word.word:
            if char in word.guessed:
                word_out += char
            else:
                word_out += "_ "
                failedChars += 1
        if failedChars == 0:
            msg = "Rätsel gelöst: %s - das Spiel ist beendet!" % word_out
            del self.words[channel]
        elif word.tries_left == 0:
            msg = "Keine Versuche mehr übrig. Das richtige Wort wäre  %s  gewesen - das Spiel ist beendet!" % word.word
            del self.words[channel]
        else:
            msg = "%s  Verbleibende Rateversuche: %d" % word_out, word.tries_left
        connection.channel_privmsg(msg, channel)
