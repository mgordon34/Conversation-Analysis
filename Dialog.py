import nltk.corpus
from nltk.text import Text
from nltk.corpus import sentiwordnet as swn
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

class Dialog:

    def __init__(self, st, c, d, t, s, r, sa):
        self.speaker = s
        self.recipient = r
        self.stamp = st
        self.content = c
        self.date = d
        self.time= t
        self.startsAt = sa

    def do(self):
        print "Hello World"

if __name__ == '__main__':
    fi = open("AbbottCostello.txt")
    cnt = 1
    speakers = {"Abbott": [], "Costello": []}
    for line in fi.readlines():
        a = line.split(":")
        di = None
        if len(a) < 1:
            continue
        elif a[0] == "Abbott":
            di = Dialog(None, a[1], None, cnt, a[0], "Costello:", None)
            speakers[a[0]].append(di)
        elif a[0] == "Costello":
            di = Dialog(None, a[1], None, cnt, a[0], "Abbott:", None)
            speakers[a[0]].append(di)
        cnt += 1



    """
        for k in speakers.keys():
        print k
        for diag in speakers[k]:
            print diag.content
    """

    fi.close()
    sid = SentimentIntensityAnalyzer()
    print "++++++++++++++++++++++++++++++++++++++++++"
    for diag in speakers["Abbott"]:
        sentence = diag.content
        print sentence
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            print ('{0} : {1}, '.format(k, ss[k]))
        print "++++++++++++++++++++++++++++++++++++++++++"

    sid = SentimentIntensityAnalyzer()
    print "*********************************************"
    for diag in speakers["Costello"]:
        sentence = diag.content
        print sentence
        ss = sid.polarity_scores(sentence)
        for k in sorted(ss):
            print ('{0} : {1}, '.format(k, ss[k]))
        print "******************************************"
