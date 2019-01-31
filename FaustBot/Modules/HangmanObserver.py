
from FaustBot.Communication.Connection import Connection
from FaustBot.Modules.PrivMsgObserverPrototype import PrivMsgObserverPrototype
from collections import defaultdict

class HangmanObserver(PrivMsgObserverPrototype):
    @staticmethod
    def cmd():
        return ['.guess', '.word', '.stop','.hint','.score','.spielregeln']

    @staticmethod
    def help():
        return 'hangman game'

    def __init__(self):
        super().__init__()
        self.word = ''
        self.guesses = ['-','/',' ','_']
        self.leftTrys = 0
        self.wrongGuesses = []
        self.score = defaultdict(int)
        self.worder = ''

    def update_on_priv_msg(self, data, connection: Connection):
        if data['message'].find('.guess ') != -1:
            self.guess(data,connection)
            return
        if data['message'].find('.word ') != -1:
            self.takeword(data, connection)
        if data['message'].find('.stop') != -1 and not data['message'].find('.stophunt') != -1:
            connection.send_channel("Spiel gestoppt. Das Wort war: " + self.word)
            self.word = ''
            self.guesses = []
            self.leftTrys = 0
            self.wrongGuesses =[]
            self.worder =''
        if data['message'].find('.hint') != -1:
            self.hint(data, connection)
        if data['message'].find('.score') != -1:
            self.printScore(data, connection)
        if data['message'].find('.spielregeln') != -1:
            self.spielregeln(data, connection)

    def printScore (self,data,connection):
        connection.send_back(data['nick']+" hat einen Score von: "+str(self.score[data['nick']]), data)
    def hint(self,data,connection):
        wrongGuessesString = "Falsch geratene Buchstaben bis jetzt: "
        for w in self.wrongGuesses:
            if w == self.wrongGuesses[0]:
                wrongGuessesString += w
            else:
                wrongGuessesString += "," + w
        connection.send_back(wrongGuessesString, data)

    def guess(self, data,connection):
        if data['channel'] != connection.details.get_channel():
            connection.send_back("Sorry kein raten im Query", data)
            return
        tried =  data['message'].split(' ')[1].upper()
        if self.leftTrys < 1:
            connection.send_channel("Flüstere mir ein neues Wort mit .word WORT")
            return
        if tried == self.word:
            self.score[data['nick']]+=self.countMissing()+5
            self.word = ''
            connection.send_channel("Das ist korrekt: "+ tried)
            return
        if tried in self.word:
            self.score[data['nick']] += 1
            self.guesses.append(tried)
        else:
            self.leftTrys -= 1
            self.score[data['nick']] -= 1
            self.wrongGuesses.append(tried)
        connection.send_channel(self.prepareWord(data))

    def takeword(self, data, connection):
        if self.word == '':
            log = open('HangmanLog','a')
            log.write(data['nick']+' ; '+data['message'].split(' ')[1].upper()+'\n')
            log.close
            self.word = data['message'].split(' ')[1].upper()
            self.guesses = ['-','/',' ','_']
            self.wrongGuesses = []
            self.leftTrys = 11
            connection.send_back( "Danke für das Wort, es ist nun im Spiel!", data)
            connection.send_channel("Das Wort ist von: "+data['nick'])
            self.worder = data['nick']
            connection.send_channel(self.prepareWord(data))
        else:
            connection.send_back("Sorry es läuft bereits ein Wort", data)

    def prepareWord(self, data):
        outWord = ""
        failedChars = 0
        for char in self.word:
            if char in self.guesses:
                outWord += char + " "
            else:
                outWord += "_ "
                failedChars += 1
        if failedChars == 0:
            outWord = "Das ist korrekt: "+self.word
            self.score[data['nick']] += 5
            self.word = ''
            return outWord
        if self.leftTrys == 0:
            self.score[self.worder] += 5
            outWord = "Das richtige Wort wäre gewesen:" + self.word
            self.word = ''
            return outWord
        outWord += "Verbleibende Rateversuche: "+str(self.leftTrys)
        return outWord

    def countMissing(self):
        failedChars = 0
        for char in self.word:
            if char not in self.guesses:
                failedChars += 1
        return failedChars

    def spielregeln(self, data, connection):
        connection.send_back("""Wort starten mit ".word Wort" im Query mit dem Bot""", data)
        connection.send_back("""Raten mit ".guess Buchstabe" im Channel""", data)
        connection.send_back("""Geraten werden können einzelne Buchstaben oder das ganze Wort.""", data)
        connection.send_back("""Alle dürfen durcheinander raten. Es gibt keine Reihenfolge.""", data)
        connection.send_back("""".hint" gibt alle bereits falsch geratenen Buchstaben aus.""", data)
        connection.send_back("""Bei 2 verbleibenden Versuchen darf nach einem Tipp vom Steller des Wortes gefragt werden.""", data)
        connection.send_back("""Wer ein Wort errät, darf das nächste stellen.""" , data)
        connection.send_back("""Wird ein Wort nicht gelöst, darf derjenige, der es gestellt hat, nochmal.""" , data)
        connection.send_back("""Zulässig sind alle Wörter, die deutsch oder im deutschen Sprachraum geläufig sind, mit Ausnahme von fsk18 Begriffen (diese dürfen in #autistenchat-fsk18 gespielt werden, sofern kein Thema läuft).""" , data)
        connection.send_back("""Ein richtig geratener Buchstabe gibt einen Punkt, eine lösung 5 und ein falscher einenen Punkt abzug, die Aktuelle Score kann mit ".score" abgefragt werden""" , data)