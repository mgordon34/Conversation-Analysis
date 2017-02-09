from nltk.sentiment.vader import SentimentIntensityAnalyzer
import Dialog
import string
import TextParsing
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from scipy.interpolate import interp1d
from plotly.graph_objs import *
import plotly.plotly as py

class Analyze:
    """
    init goes ahead and populates the dictionary of emotions that will be used to analyze documents
    emotionDict works as follows:
        keys: anticipation, fear, anger, trust, surprise, sadness, joy, disgust
        values: Dictionaries whose keys are the words and values are the score of that word
        example: emotionDict["anticipation"]["kim"] ==> 0.816092414706127
    """
    def __init__(self):
        self.sid = SentimentIntensityAnalyzer()
        self.emotionDict = {"anticipation":{}, "fear":{}, "anger":{}, "trust":{}, "surprise":{}, "sadness":{}, "joy":{}, "disgust":{}}
        #self.twittDict = {}
        #Keys: words , values: number ranging from -1 to 1. -1 is negative and 1 is positive
        self.sentimentDict = {}
        fi = open("NRC-Hashtag-Emotion-Lexicon-v0.2/NRC-Hashtag-Emotion-Lexicon-v0.2.txt")
        for line in fi.readlines():
            arr = line.split()
            if len(arr[1].split("#")) > 1:
                self.emotionDict[arr[0]][arr[1].split("#")[1]] = float(arr[2])
            else:
                self.emotionDict[arr[0]][arr[1]] = float(arr[2])
                #print arr[0], arr[1], arr[2]
        fi.close()
        fi = open("NRC-Hashtag-Emotion-Lexicon-v0.2/SemEval2015-English-Twitter-Lexicon.txt")
        for  line in fi.readlines():
            arr = line.split()
            #if there is a '#' in front of the words we want to disregard it.
            if len(arr[1].split("#")) > 1:
                self.sentimentDict[arr[1].split("#")[1]] = float(arr[0])
        fi.close()
        fi = open("vader_lexicon.txt")
        #Vader has the values such that -4 is really negative and 4 is really postiive
        for line in fi.readlines():
            arr = line.split()
            # if there is a '#' in front of the words we want to disregard it.
            #if len(arr[1].split("#")) > 1:
            #print arr[0].lower(), float(arr[1])/4
            self.sentimentDict[arr[0].lower()] = float(arr[1])/4 #normalize
        fi.close()
        fi = open("vaderEmoticons.txt")
        # Vader has the values such that -4 is really negative and 4 is really postiive
        for line in fi.readlines():
            arr = line.split()
            # if there is a '#' in front of the words we want to disregard it.
            # if len(arr[1].split("#")) > 1:
            self.sentimentDict[arr[0].lower()] = float(arr[1]) / 4  # normalize
        self.sentimentDict["( '}{' )"] = 1.6/4
        fi.close()
        """
        for emotion in self.emotionDict.keys():
            print emotion
            eDict = self.emotionDict[emotion]
            for word in eDict.keys():
                print emotion, word, eDict[word]
        """


    """
    Takes in a TextParsing (tp) and a speaker that is in the text.
    Outputs an array of tuples (content, [compund, negative, neutral, postive])
    All of the content in the output is spoken by the designated speaker
    """
    def getSentimentData(self, tp, speaker):
        lines = []
        #print "++++++++++++++++++++++++++++++++++++++++++"
        for i in tp.speakerDict[speaker]:
            sentence = tp.dialogues[i].content
            # ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line of Abbott's
            ss = self.sid.polarity_scores(sentence)
            lines.append((sentence ,[ss['compound'], ss['neg'], ss['neu'], ss['pos']]))
        return lines


    """
    takes in a Text Parsing, the speaker's name, and the emotion you desire
    Outputs a list of the speaker's emotion scores for all of his lines.
    Each line is broken into an array of tuples where the first value is the word and the second is the emotion score.
    """
    def getEmotionSpeaker(self, tp, speaker, emote):
        lines = []
        # print "++++++++++++++++++++++++++++++++++++++++++"
        eDict = self.emotionDict[emote]
        for i in tp.speakerDict[speaker]:
            sent = tp.dialogues[i].content.split()
            line = []
            for word in sent:
                try:
                    line.append([word.lower(),eDict[word.lower()]])
                except:
                    line.append([word.lower(), 0.0])
            lines.append(line)
            #print line
        return lines


    """
    populates a dialog's emotion scores array
    """
    def popDialogEmotion(self, tp):
        for diag in tp.dialogues:
            sent = diag.content.split()
            #print sent
            #print "___________________________________________________"
            for e in self.emotionDict.keys():
                eDict = self.emotionDict[e]
                for word in sent:
                    try:
                        diag.emotions[e].append(eDict[word.lower()])
                    except:
                        diag.emotions[e].append(0.0)
                #print e, diag.getAverageEmotion(e), diag.emotions[e]
            #print "___________________________________________________"


    """
    Sets the sentiment of the conversation no matter who the speaker is.
    Sentiment analysis on all of the lines.
    """
    def setDialogSentiment(self, tp):
        lines = []
        for diag in tp.dialogues:
            sentence = diag.content
            # ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line of Abbott's
            ss = self.sid.polarity_scores(sentence)
            #for k in sorted(ss):
                #print ('{0} : {1}, '.format(k, ss[k]))
            diag.sentiment = [ss['compound'], ss['neg'], ss['neu'], ss['pos']]
            #print sentence, diag.sentiment
            lines.append([ss['compound'], ss['neg'], ss['neu'], ss['pos']])
        return lines

    def plotlyEmotion(self, tp, speakerArray, emote):
        if len(speakerArray) < 2:
            print "please enter in two or more speakers"
            return
        k = 0
        traces = []
        for sp in speakerArray:
            xs = []
            ys = []
            for i in tp.speakerToClass[sp].lines:
                val = float(tp.dialogues[i].getAverageEmotion(emote))
                if val != 0:
                    xs.append(float(i))
                    ys.append(val)
            trace = Scatter(
                x=xs,
                y=ys
            )
            traces.append(trace)
            # diff.append((sentence, [ss['compound'], ss['neg'], ss['neu'], ss['pos']]))
            k += 1
        data = Data(traces)
        py.plot(data, filename='testy-plotly')


    def scatterGraphEmotion(self, tp, speakerArray, emote):
        funcArr = []
        if len(speakerArray) < 2:
            print "please enter in two or more speakers"
            return
        k = 0
        for sp in speakerArray:

            funcArr.append([[], []])
            for i in tp.speakerToClass[sp].lines:
                val = float(tp.dialogues[i].getAverageEmotion(emote))
                if val != 0:

                    funcArr[k][0].append(float(i))
                    funcArr[k][1].append(val)
                # diff.append((sentence, [ss['compound'], ss['neg'], ss['neu'], ss['pos']]))
            k += 1
        py.plot(data, filename='basic-line')
        #PY-Plot stuff
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        colors = cm.rainbow(np.linspace(0, 1, len(funcArr)))
        plt.ylabel('sentiment score')
        plt.xlabel("line number")
        plt.title(emote)
        for i in range(len(funcArr)):
            # xnew = np.linspace(0, 65, endpoint=True)
            ax1.scatter(funcArr[i][0], funcArr[i][1], s=10, c=colors[i], marker="s", label=speakerArray[i])
            # f = interp1d(funcArr[i][0], funcArr[i][1])
            # plt.plot(funcArr[i][0], funcArr[i][1], 'o',funcArr[i][0], f(funcArr[i][1]))
            # plt.plot(funcArr[i][0], funcArr[i][1], 'o', xnew, f(xnew), '-')
        # plt.legend(speakerArray, loc='best')
        plt.legend(loc='upper left')
        plt.show()
    """
    Creates a scatter plot of the speakers in teh speaker array and the sentiment desired. 
    possible sentiments: pos, neg, neu, compund
    """
    def scatterPlotSentiment (self, tp, speakerArray, sentiment):
        funcArr = []
        if len(speakerArray) < 2:
            print "please enter in two or more speakers"
            return
        k = 0
        for sp in speakerArray:
            funcArr.append([[],[]])
            #print sp, len(tp.speakerDict[sp])
            #print sp.lines
            for i in tp.speakerToClass[sp].lines:
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
     the overall sentiment of the conversation (compound, negative, neutral, positive)
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
    Calculates the average compound, negative, neutral and positive scores of all speakers in the conversation to determine
    the overall sentiment of the conversation (compound, negative, neutral, positive)
    Returns a tuple of sentiment values:
    """
    def getVaderSentimentWords(self, tp):
        # (compoud, neg, neu, pos)
        ls = [0, 0, 0, 0]
        retArr = []
        for i in range(len(tp.dialogues)):
            # ss is a dictionary containing the compound, negative (neg) and positive sentiment rating of a single line
            sent = tp.dialogues[i].content
            sData = []
            for w in sent.split():
                #wd = wd.translate(string.maketrans("", ""), string.punctuation)
                ss = self.sid.polarity_scores(w)
                sData.append(ss)
                #print w, ss
            retArr.append(sData)
            for i, k in enumerate(["compound", "neg", "neu", "pos"]):
                ls[i] += ss[k]
        for i in range(len(ls)):
            ls[i] = ls[i] / len(tp.dialogues)
        return retArr

    """
    method that calculates the desired emotion scores for each sentence said by the desired speaker.
    String emotion: anticipation, fear, anger, trust, surprise, sadness, joy, disgust
    Returns a list of dictionaries corresponding to the emotions of the sentence as stored in Dialog
    """
    def getAverageEmotionScore(self, speaker, emotion):
        lines = tp.speakerDict[speaker]
        diags = tp.dialogues
        val = 0
        cnt = 0
        for i in lines:
            for k in diags[i].emotions[emotion]:
                val += k
                cnt += 1
        if cnt == 0:
            val = 0
        else:
            val = val/cnt
        return val

    """
    Gets the overall sentiment according to the vader text document. Scores go from a range of -1 to 1.
    -1 is negative----- 0 neutral ----- 1 positive
    Outpus a list of lists of list. Each list is a sentence in the converstation. Inside is each word of the sentence
    along with the score.
    ex: [['good', 0.475], ['evening', 0.475], ['guys', 0.475]]
    """
    def getSentimentOfWords(self, tp):
        retArr = []
        for diag in tp.dialogues:
            sentence = diag.content
            words = sentence.split()
            sentVader = []
            val = 0
            for i in range(len(words)):
                wd = words[i].lower()
                #wd = wd.translate(string.maketrans("", ""), string.punctuation)
                try:
                    val = self.sentimentDict[wd]
                    sentVader.append([wd, val])
                except:
                    sentVader.append([wd, val])
            retArr.append(sentVader)
            #print sentVader
        return retArr

    """
       Uses the Twitter Dictionary to get the overall sentiment score of a word. -1 is very negative while 1 is positive


       def getTwitterDictSentiment(self, tp):
           retArr = []
           for diag in tp.dialogues:
               sentence = diag.content
               words = sentence.split()
               sentTwit = []
               val = 0
               for i in range(len(words)):
                   if words[i] == "don't":
                       w = words[i+1]
                       wd = words[i] + " " + w.translate(string.maketrans("",""), string.punctuation)
                       wd.lower()
                   else:
                       wd = words[i].lower()
                       wd = wd.translate(string.maketrans("",""), string.punctuation)
                   try:
                       val = self.twittDict[wd]
                       sentTwit.append([wd, val])
                   except:
                       sentTwit.append([wd, val])
               retArr.append(sentTwit)
               #print sentTwit
           return retArr
       """

if __name__ == '__main__':
    tp = TextParsing.TextParsing("exampleData.rtf")
    a = Analyze()
    a.popDialogEmotion(tp)
    #a.getSentimentOfWords(tp)
    speakers = tp.speakerDict.keys()
    #a.getEmotionSpeaker(tp, speakers[0], "anticipation")
    a.lineGraphSentiment(tp, speakers, "joy")
    #a.scatterPlotSentiment(tp, speakers, "pos")
    #print speakers[0], a.getAverageEmotionScore(speakers[0], "anticipation")

    #a.getConversationSentiment(tp)
    #a.setDialogSentiment(tp)
    #a.getTwitterDictSentiment(tp)
    #a.getSentimentTextVader(tp)
    #a.getVaderSentimentWords(tp)
    #print a.getAverageScores(tp)
    #print a.getSentimentData(tp, "Tempus")
    #print a.getConversationSentiment(tp)
    #a.getDifference(tp, ["Tempus", "Bunnycrusher", "Daner"], "pos")
