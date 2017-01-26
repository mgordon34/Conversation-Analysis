import Dialog
from nltk.sentiment.vader import SentimentIntensityAnalyzer
fi = open("AbbottCostello.txt")
cnt = 1
speakers = {"Abbott": [], "Costello": []}

"""
The following code uses the VADER sentiment analysis tool.
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
"""

#Reading in the Abbott and Costello Document
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

fi.close()

sid = SentimentIntensityAnalyzer()
#diff contains the difference between Abbot's and Costello's sentiment rankings
diff = []

#abLines is an array dictionaries contains Abbot's sentiment rankings. One entry in abLines corresponds to one line in the conversation
abLines = []

#costLines is an array dictionaries contains Costello's sentiment rankings. One entry in abLines corresponds to one line in the conversation
costLines = []

print "++++++++++++++++++++++++++++++++++++++++++"
for diag in speakers["Abbott"]:
    sentence = diag.content
    print sentence
    #ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line of Abbott's
    ss = sid.polarity_scores(sentence)
    abLines.append(ss)
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
    #ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line of Costello's
    ss = sid.polarity_scores(sentence)
    costLines.append(ss)
    #print ss
    for k in sorted(ss):
        print ('{0} : {1}, '.format(k, ss[k]))
    diff[cnt] = [abs(diff[cnt][0]-ss['compound']), abs(diff[cnt][1] - ss['neg']), abs(diff[cnt][2]-ss['neu']), abs(diff[cnt][3]-ss['pos'])]
    print "******************************************"
    cnt +=1
fi.close()
for d in diff:
    print d