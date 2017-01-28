from nltk.sentiment.vader import SentimentIntensityAnalyzer
import Dialog
import TextParsing
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

class Analyze:
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()


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

    #TODO: getDifference does not work
    def getDifference (self, tp, speakerArray, sentiment):
        funcArr = []
        diff = []
        if len(speakerArray) < 2:
            print "please enter in two or more speakers"
            return
        k = 0
        for sp in speakerArray:
            funcArr.append([[],[]])
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
        for i in range(len(funcArr)):
            ax1.scatter(funcArr[i][0], funcArr[i][1], s=10,c=colors[i], marker="s", label=speakerArray[i])
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

if __name__ == '__main__':
    tp = TextParsing.TextParsing("exampleData.rtf")
    a = Analyze()
    print a.getAverageScores(tp)
    #print a.getSentimentData(tp, "Tempus")
    print a.getConversationSentiment(tp)
    a.getDifference(tp, ["Tempus", "Bunnycrusher"], "pos")