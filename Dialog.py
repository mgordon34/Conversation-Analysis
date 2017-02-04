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
        self.sentiment = [0.0, 0.0, 0.0,0.0]

    """
    Calculates the average emotion score for the content of the sentence.
    String emotion: anticipation, fear, anger, trust, surprise, sadness, joy, disgust
    Adds all of the values together and divides by the number of non-zero values
    Outputs a float value representing the average emotion
    """
    def getAverageEmotion(self, emotion):
        if self.emotions[emotion] < 1:
            return 0.0
        n = 0
        total = 0
        for val in self.emotions[emotion]:
            if val > 0:
                n +=1
                total += val
        if val > 0:
            return total/n
        else:
            return 0.0