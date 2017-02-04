#Basic Dialog class that holds the information found in one row of the inputted data file.
class Dialog:

    def __init__(self, st, c, d, t, s, r, sa):
        self.speaker = s
        self.recipient = r
        self.stamp = st
        self.content = c
        self.date = d
        self.time= t
        self.startsAt = sa
        self.emotions =  {"anticipation":[], "fear":[], "anger":[], "trust":[], "surprise":[], "sadness":[], "joy":[], "disgust":[]}


