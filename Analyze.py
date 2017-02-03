from nltk.sentiment.vader import SentimentIntensityAnalyzer
import Dialog
import TextParsing
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from scipy.interpolate import interp1d

class Analyze:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()
        self.emotionDict = {"anticipation":{}, "fear":{}, "anger":{}, "trust":{}, "surprise":{}, "sadness":{}, "joy":{}, "disgust":{}}
        fi = open("NRC-Hashtag-Emotion-Lexicon-v0.2/NRC-Hashtag-Emotion-Lexicon-v0.2.txt")
        for line in fi.readlines():
            arr = line.split()
            if len(arr[1].split("#")) > 1:
                self.emotionDict[arr[0]][arr[1].split("#")[1]] = float(arr[2])
            else:
                self.emotionDict[arr[0]][arr[1]] = float(arr[2])
        fi.close()

        for emotion in self.emotionDict.keys():
            print emotion
            eDict = self.emotionDict[emotion]
            for word in eDict.keys():
                print emotion, word, eDict[word]


    """
    Takes in a TextParsing (tp) and a speaker that is the text.
    Outputs an array of tuples (content, [compund, negative, neutral, postive])
    All of the content in the output is spoken by the designated speaker
    """
    def getSentimentData(self, tp, speaker):
        # diff contains the difference between Abbot's and Costello's sentiment rankings
        lines = []
        #print "++++++++++++++++++++++++++++++++++++++++++"
        for i in tp.speakerDict[speaker]:
            sentence = tp.dialogues[i].content
            # ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line of Abbott's
            ss = self.sid.polarity_scores(sentence)
            #for k in sorted(ss):
            #    print ('{0} : {1}, '.format(k, ss[k]))
            lines.append((sentence ,[ss['compound'], ss['neg'], ss['neu'], ss['pos']]))
        return lines

    """
    Gets the sentiment of the conversation no matter who the speaker is.
    Sentiment analysis on all of the lines.
    """
    def getConversationSentiment(self, tp):
        lines = []
        for diag in tp.dialogues:
            sentence = diag.content
            # ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line of Abbott's
            ss = self.sid.polarity_scores(sentence)
            #for k in sorted(ss):
                #print ('{0} : {1}, '.format(k, ss[k]))
            lines.append([ss['compound'], ss['neg'], ss['neu'], ss['pos']])
        return lines

    """
    Creates a scatter plot of the speakers in teh speaker array and the sentiment desired. 
    possible sentiments: pos, neg, neu, compund
    """
    def getDifference (self, tp, speakerArray, sentiment):
        funcArr = []
        diff = []
        if len(speakerArray) < 2:
            print "please enter in two or more speakers"
            return
        k = 0
        for sp in speakerArray:
            funcArr.append([[],[]])
            print sp, len(tp.speakerDict[sp])
            for i in tp.speakerDict[sp]:
                sentence = tp.dialogues[i].content
                # ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line of Abbott's
                ss = self.sid.polarity_scores(sentence)
                #print sentence, i
                funcArr[k][0].append(float(i))
                funcArr[k][1].append(float(ss[sentiment]))
                #diff.append((sentence, [ss['compound'], ss['neg'], ss['neu'], ss['pos']]))
            k += 1

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        colors = cm.rainbow(np.linspace(0, 1, len(funcArr)))
        plt.ylabel('sentiment score')
        plt.xlabel("line number")
        plt.title(sentiment)
        for i in range(len(funcArr)):
            #xnew = np.linspace(0, 65, endpoint=True)
            ax1.scatter(funcArr[i][0], funcArr[i][1], s=10,c=colors[i], marker="s", label=speakerArray[i])
            #f = interp1d(funcArr[i][0], funcArr[i][1])
            #plt.plot(funcArr[i][0], funcArr[i][1], 'o',funcArr[i][0], f(funcArr[i][1]))
            #plt.plot(funcArr[i][0], funcArr[i][1], 'o', xnew, f(xnew), '-')
        #plt.legend(speakerArray, loc='best')
        plt.legend(loc='upper left')
        plt.show()


    """
     Calculates the average compound, negative, neutral and positive scores of all speakers in the conversation to determine
     the overall sentiment of the converstation (compound, negative, neutral, positive)
     Returns a tuple of sentiment values:
    """
    def getAverageScores(self, tp):
        #(compoud, neg, neu, pos)
        ls = [0,0,0,0]
        for i in range(len(tp.dialogues)):
            # ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line
            ss = self.sid.polarity_scores(tp.dialogues[i].content)
            for i,k in enumerate (["compound", "neg", "neu", "pos"]):
                ls[i] += ss[k]

        for i in range(len(ls)):
            ls[i] = ls[i]/len(tp.dialogues)
        return tuple(ls)

    """
    method that calculates the desired emotion inputted. Possible emotions include:
    anticipation, fear, anger, trust, surprise, sadness, joy, disgust
    """
    def getEmotionScores(self):
       pass

if __name__ == '__main__':
    tp = TextParsing.TextParsing("exampleData.rtf")
    a = Analyze()

    #print a.getAverageScores(tp)
    #print a.getSentimentData(tp, "Tempus")
    #print a.getConversationSentiment(tp)
    #a.getDifference(tp, ["Tempus", "Bunnycrusher", "Daner"], "pos")
