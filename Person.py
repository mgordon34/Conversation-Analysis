import nltk
from nltk import word_tokenize
import json
"""
The person class will hold the following information.


        # most Frequent words
        # Speaker's average emotion between every other speaker.
        speaker's average emotion: dictionary of the 8 emotions we calculate
        speaker's average sentiment: array of vader sentiment scores
        speaker's name: string
        speaker's lines: lines is a list of indices into the text parsing's dialog array
        speaker's contribution to the conversation i.e. how much they spoke compared to everyone else


"""
class Person:

    def __init__(self, n ,l):
        self.name = n
        self.lines = l
        self.text = None
        self.emotionAverage =  {"anticipation":0.0, "fear":0.0, "anger":0.0, "trust":0.0, "surprise":0.0, "sadness":0.0, "joy":0.0, "disgust":0.0}
        self.sentiment = [0.0, 0.0, 0.0, 0.0]
        self.freqDist = None
        self.contribution = 0.0

    # Concordance tells you all of the times the word is in said in the conversation along with its context
    def getConcordance(self, word):
        return self.text.concordance(word)

    # counts the number of time the word was said in the conversation
    def getFrequecyOfWord(self, word):
        return self.text.count(word)

    # Returns a list of words that only appear once
    def getHapaxes(self):
        return self.freqDist.hapaxes()

    # gets the first n common words that were spoken in the conversation
    # returns a list of tuples. ex: [(',', 176), ('the', 155), ('I', 105), ('you', 89), ('to', 85), ('it', 85), ('we', 82), ('?', 69)]
    def getNCommonWords(self, n):
        return self.freqDist.most_common(n)

    def plotlyBarFreqDist(self):
        fdist1 = self.freqDist
        xs = []
        ys = []
        for point in fdist1.most_common(50):
            #print point
            xs.append(point[0])
            ys.append(point[1])
        # data.append(json.dumps(trace, separators=(',', ':')))
        trace = {"x": xs, "y": ys, "type": "bar"}
        json_data = json.dumps(trace, separators=(",", ":"))
        return json_data

