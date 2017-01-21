import nltk
import Dialog
import datetime
#d = datetime()
#di = Dialog(None, cont, None, None, sp, ra, )
fi = open("AbbottCostello.txt")
ab = []
ca = []
cnt = 1
speakers = {"Abbott:": [], "Costello:":[]}
for line in fi.readlines():
    a = line.split()
    if a[0] == "Abbott:":
        di = Dialog(None, line[1:], None, cnt, a[0], "Costello:", None)
    if a[0] == "Costello:":
        di = Dialog(None, line[1:], None, cnt, a[0], "Abbott:", None)
    speakers[a[0]].append(di)
    print a


fi.close()