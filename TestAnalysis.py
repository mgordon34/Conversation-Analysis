import Dialog
import nltk.corpus
from nltk.text import Text
from nltk.corpus import sentiwordnet as swn
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
#di = Dialog(None, cont, None, None, sp, ra, )
fi = open("AbbottCostello.txt")
cnt = 1
speakers = {"Abbott": [], "Costello": []}
for line in fi.readlines():
    a = line.split(":")
    di = None
    if len(a) < 1:
        continue
    elif a[0] == "Abbott":
        di = Dialog.Dialog(None, a[1], None, cnt, a[0], "Costello:", None)
        speakers[a[0]].append(di)
    elif a[0] == "Costello":
        di = Dialog.Dialog(None, a[1], None, cnt, a[0], "Abbott:", None)
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
diff = []

print "++++++++++++++++++++++++++++++++++++++++++"
for diag in speakers["Abbott"]:
    sentence = diag.content
    print sentence
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        print ('{0} : {1}, '.format(k, ss[k]))
    diff.append([ss['compound'], ss['neg'], ss['neu'], ss['pos']])

    print "++++++++++++++++++++++++++++++++++++++++++"

i = len(diff)
cnt = 0
sid = SentimentIntensityAnalyzer()
print "*********************************************"
for diag in speakers["Costello"]:
    sentence = diag.content
    print sentence
    ss = sid.polarity_scores(sentence)
    print ss
    for k in sorted(ss):
        print ('{0} : {1}, '.format(k, ss[k]))
    diff[cnt] = [abs(diff[cnt][0]-ss['compound']), abs(diff[cnt][1] - ss['neg']), abs(diff[cnt][2]-ss['neu']), abs(diff[cnt][3]-ss['pos'])]
    print "******************************************"
    cnt +=1
fi.close()
for d in diff:
    print d