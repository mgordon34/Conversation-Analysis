from nltk.sentiment.vader import SentimentIntensityAnalyzer
import Dialog
import TextParsing

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
        print "++++++++++++++++++++++++++++++++++++++++++"
        for i in tp.speakerDict[speaker]:
            sentence = tp.dialogues[i].content
            print sentence
            # ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line of Abbott's
            ss = self.sid.polarity_scores(sentence)
            for k in sorted(ss):
                print ('{0} : {1}, '.format(k, ss[k]))
            lines.append((sentence ,[ss['compound'], ss['neg'], ss['neu'], ss['pos']]))
        return lines

    def getDifference (self, tp, speakerArray):
        #diff contains the difference between Abbot's and Costello's sentiment rankings
        diff = []
        for sp in tp.speakerDict.keys():
            for i in tp.speakerDict[sp]:
                sentence = tp.dialogues[i].content
                print sentence
                # ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line of Abbott's
                ss = self.sid.polarity_scores(sentence)
                for k in sorted(ss):
                    print ('{0} : {1}, '.format(k, ss[k]))
                diff.append((sentence, [ss['compound'], ss['neg'], ss['neu'], ss['pos']]))

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
    print a.getSentimentData(tp, "Tempus")