#Basic Dialog class that holds the information found in one row of the inputted data file.
"""
    - Speaker (string) The name of the speaker
    - Line number (integer)  the order number of the line
    - Timespan (string) time range when the speaker was talking
    - Content (string) What the speaker said i.e. their sentence
    - Date (string) The date at which the conversation was
    - Time (string) The time of day the conversation took place
    - Recipient (string) Who the speaker was talking to. (labeled "all" if directed at everyone in the group)
    - emotions (dictionary) a dictionary that holds information as follows: Keys are the desired emotion that you wish
    to track. The values are an array of float values that correspond to the emotion score for that word at the index
    - sentiment array that contains floats that represents the contents overall positive, negative and neutral output.
    All scores range from 0 - 1. 1 being the most like that sentiment, 0 being unlike that sentiment.
    The compound score is the overall sentiment score of the sentence. 0 being very negative, 1 being very positive.
        ["compound", "neg", "neu", "pos"]
        -> At index 0 -> Compound Score
        -> At index 1 -> Negative Score
        -> At index 2 _> Neutral Score
        -> At index 3 -> Positive Score

"""
class Dialog:

    def __init__(self, st, c, d, t, s, r, sa):
        self.speaker = s
        self.recipient = r
        self.stamp = st
        self.content = c
        #TODO make date a Date Python Object
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
        if n > 0:
            return total/n
        else:
            return 0.0