from FaustBot.Model.HanDatabaseProvider import HanDatabaseProvider
import csv
HanDBProvider = HanDatabaseProvider()
wordList = open("HangmanLog")
wordListWords = csv.reader(wordList, delimiter=';', quotechar='|')
randomChoicePool = []
for word in wordListWords:
    print(word)
    print(word[1].strip())
    HanDBProvider.addWord(word[1].strip())
