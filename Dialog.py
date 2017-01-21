import nltk.corpus
from nltk.text import Text
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
    raw = fi.read()
    tokens = nltk.word_tokenize(raw)
    t = nltk.Text(tokens)
    t.similar("")
    fi.close()
    fi = open("AbbottCostello.txt")
    cnt = 1
    speakers = {"Abbott:": [], "Costello:": []}
    for line in fi.readlines():
        a = line.split()
        di = None
        if len(a) < 1:
            continue
        elif a[0] == "Abbott:":
            di = Dialog(None, line[1:], None, cnt, a[0], "Costello:", None)
        elif a[0] == "Costello:":
            di = Dialog(None, line[1:], None, cnt, a[0], "Abbott:", None)
        speakers[a[0]].append(di)
        cnt += 1
    fi.close()

