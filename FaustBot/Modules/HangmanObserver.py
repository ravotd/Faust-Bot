
from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype


class HangmanObserver(PrivMsgObserverPrototype):
    def __init__(self):
        self.word = ''
        self.guesses = []
        self.leftTrys = 0

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.guess') != -1:
            self.guess(data,connection)
        if data['message'].find('.word') != -1:
            self.takeword(data, connection)

    def guess(self, data,connection):
        tried =  data['message'].split(' ')[1].upper()#
        if self.leftTrys < 1:
            connection.send_channel("Flüstere mir ein neues Wort mit .word WORT")
            return
        if tried == self.word:
            self.word = ''
            connection.send_channel("Korrekt: "+ tried)
            return
        if tried in self.word:
            self.guesses += tried
        else:
            self.leftTrys -= 1
        connection.send_channel(self.prepareWord())

    def takeword(self, data, connection):
        if self.word == '':
            self.word = data['message'].split(' ')[1].upper()
            self.guesses = []
            self.leftTrys = 5
            connection.send_channel(self.prepareWord())
        else:
            connection.send_back("Sorry es läuft bereits ein Wort", data)

    def prepareWord(self):
        outWord = ""
        failedChars = 0
        for char in self.word:
            if char in self.guesses:
                outWord += char + " "
            else:
                outWord += "_ "
                failedChars += 1
        if failedChars == 0:
            self.word = ''
        if self.leftTrys == 0:
            outWord = "Das richtige Wort wäre gewesen:" + self.word
            self.word = ''
            return outWord
        outWord += "Verbleibende Rateversuche: "+str(self.leftTrys)
        return outWord
