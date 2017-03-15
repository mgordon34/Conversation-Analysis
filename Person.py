import nltk
from nltk import word_tokenize
class Person:

    def __init__(self, n ,l):
        self.name = n
        self.lines = l
        self.text = None
        self.emotionAverage =  {"anticipation":0.0, "fear":0.0, "anger":0.0, "trust":0.0, "surprise":0.0, "sadness":0.0, "joy":0.0, "disgust":0.0}
        self.sentiment = [0.0, 0.0, 0.0,0.0]
        self.freqDist = None
        #self.colors = []


        # Concordance tells you all of the times the word is in said in the conversation along with its context
        def getConcordance(self, word):
            return self.text.concordance(word)

        # counts the number of time the word was said in the conversation
        def getFrequecyOfWord(self, word):
            return self.text.count(word)

        # Returns a list of words that only appear once
        def getHapaxes(self):
            return self.freqDist.hapaxes()




