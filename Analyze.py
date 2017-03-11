"""
[2] Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
[3] Sentiment Analysis of Short Informal Texts. Svetlana Kiritchenko, Xiaodan Zhu and Saif Mohammad. Journal of Artificial Intelligence Research, volume 50, pages 723-762, August 2014.
[4] NRC-Canada: Building the State-of-the-Art in Sentiment Analysis of Tweets, Saif M. Mohammad, Svetlana Kiritchenko, and Xiaodan Zhu, In Proceedings of the seventh international workshop on Semantic Evaluation Exercises (SemEval-2013), June 2013, Atlanta, USA.
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import TextParsing
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
import json
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
        self.sentimentDict = {}
        self.emotionDict = {"anticipation":{}, "fear":{}, "anger":{}, "trust":{}, "surprise":{}, "sadness":{}, "joy":{}, "disgust":{}}
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
     About the scoring:
     The 'compound' score is computed by summing the valence scores of each word in the lexicon, adjusted
     according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive).
     This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence.
     Calling it a 'normalized, weighted composite score' is accurate.
     The 'pos', 'neu', and 'neg' scores are ratios for proportions of text that fall in each category (so these
     should all add up to be 1... or close to it with float operation).  These are the most useful metrics if
     you want multidimensional measures of sentiment for a given sentence.
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

    def getDummyExample(self):
        sentence = "Hello World! I love Georgia Tech!"
        sentence2 = "Goodbye World! I HATE Georgia Tech!"
        ss1 = self.sid.polarity_scores(sentence)
        ss2 = self.sid.polarity_scores(sentence2)
        print "compound: ", ss1['compound'], " negative: ", ss1['neg'], " positive: ", ss1['pos']
        print "compound: ", ss2['compound'], " negative: ", ss2['neg'], " positive: ", ss2['pos']
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

    """
    Tester method to get the emotion scores of the desired speakers.
    speakerArray --> Array of speaker names as strings
    tp ==> TextParsing object
    emote --> the emotion desired as a string: options include:
        anticipation, fear, anger, trust, surprise, sadness, joy, disgust
    """
    # def plotlyEmotion(self, tp, speakerArray, emote):
    #     if len(speakerArray) < 2:
    #         print "please enter in two or more speakers"
    #         return
    #     k = 0
    #     traces = []
    #     for sp in speakerArray:
    #         xs = []
    #         ys = []
    #         for i in tp.speakerToClass[sp].lines:
    #             val = float(tp.dialogues[i].getAverageEmotion(emote))
    #             if val != 0:
    #                 xs.append(float(i))
    #                 ys.append(val)
    #         trace = Scatter(
    #             x=xs,
    #             y=ys,
    #             name=sp
    #         )
    #         traces.append(trace)
    #         # diff.append((sentence, [ss['compound'], ss['neg'], ss['neu'], ss['pos']]))
    #         k += 1
    #     data = Data(traces)
    #     py.plot(data, filename='testy-plotly')
    #     return data

    def plotlyEmotion(self, tp, speakerArray, emote):
        if len(speakerArray) < 2:
            print "please enter in two or more speakers"
            return
        k = 0
        traces = []
        a = Analyze()
        a.popDialogEmotion(tp)
        for sp in speakerArray:
            xs = []
            ys = []
            lines = []
            for i in tp.speakerToClass[sp].lines:
                val = tp.dialogues[i].getAverageEmotion(emote)
                # if val != 0:
                # print float(i)
                # print val
                xs.append(float(i))
                ys.append(val)
                lines.append(tp.dialogues[i].content)
            trace = {
                "type": "scatter",
                "name": sp,
                # "text": ys,
                # "hoverinfo": 'text',
                "lines": lines,
                "x": xs,
                "y": ys
                # mode='markers+lines',
                # showLine=True
            }

            # traces[sp] = trace
            # traces.append(json.dumps(trace))
            traces.append(trace)
            # diff.append((sentence, [ss['compound'], ss['neg'], ss['neu'], ss['pos']]))
            k += 1
        json_data = json.dumps(traces, separators=(',', ':'))
        # x = []
        # y = []
        # for i in tp.speakerToClass[speakerArray[0]].lines:
        #     a = Analyze()
        #     a.popDialogEmotion(tp)
        #     val = tp.dialoques[i].getAverageEmotion(emote)
        #     if val != 0:
        #         x.append(float(i))
        #         y.append(val)
        # trace = go.Scatter(
        #     x = x
        #     y = y
        #
        # )
        # py.plot(data, filename='testy-plotly')
        # print traces
        return json_data

    def plotlyEmotionTester(self, tp, speakerArray, emote):
        if len(speakerArray) < 2:
            print "please enter in two or more speakers"
            return
        k = 0
        traces = []
        for sp in speakerArray:
            xs = []
            ys = []
            print sp
            for i in tp.speakerToClass[sp].lines:
                val = float(tp.dialogues[i].getAverageEmotion(emote))
                if val != 0:
                    xs.append(float(i))
                    ys.append(val)
            print "________________________________________________________________________"
            print xs
            print ys
            print "________________________________________________________________________"
            trace = [xs, ys]

            #trace = Scatter(
            #    x=xs,
            #    y=ys,
            #    name=sp
            #)
            traces.append(trace)
            # diff.append((sentence, [ss['compound'], ss['neg'], ss['neu'], ss['pos']]))
            k += 1
        #data = Data(traces)
        #py.plot(data, filename='testy-plotly')
        return traces

    """
    Creates a scatter plot using py plot. We track all of the speakers' (inputted as strings) emotion scores
    on the given emotion
    """
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
    Creates a scatter plot of the speakers in the speaker array and the sentiment desired.
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
    def getAverageConversationScores(self, tp):
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
    Calculates the average sentiment score of all speakers in the conversation based on the Vader library
    """
    def getAverageVaderSentimentWords(self, tp):
        d = self.getVaderSentimentOfWords(tp)
        sum = 0.0
        cnt = 0
        for sent in d:
            for arr in sent:
                sum += arr[1]
                cnt += 1
        if cnt > 0:
            return sum/cnt
        else:
            return 0

    """
    method that calculates the desired emotion scores for each sentence said by the desired speaker.
    String emotion: anticipation, fear, anger, trust, surprise, sadness, joy, disgust
    Returns a list of dictionaries corresponding to the emotions of the sentence as stored in Dialog
    """
    def getAverageEmotionRemoveZerosScore(self, speaker, emotion):
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
            val = val / cnt
        return val

    """
    Gets the overall sentiment according to the vader text document. Scores go from a range of -1 to 1.
    -1 is negative----- 0 neutral ----- 1 positive
    Outputs a list of lists of list. Each list is a sentence in the converstation. Inside is each word of the sentence
    along with the score.
    ex: [['good', 0.475], ['evening', 0.475], ['guys', 0.475]]
    """
    def getVaderSentimentOfWords(self, tp):
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
        return retArr

    """
    Compares the overall emotion sp1 feels toward sp2.
    Finds all of the lines sp1 says to sp2 and finds the average emotion scores of sp1 while taking to sp2
    If you type "everyone" as sp2, it will calculate sp1's overall emotion toward the group.
    Returns a dictionary of emotions that sp1 feels while talking to sp2.
    {"anticipation":0.0, "fear":0.0, "anger":0.0,"trust":0.0, "surprise":0.0, "sadness":0.0, "joy":0.0, "disgust":0.0}
    """
    def emotAverageBwSpeakers(self,tp, sp1, sp2):
        p = False
        if sp1 == "everyone":
            print "Speaker 1 cannont be everyone"
            return {}
        lineNums = tp.speakerToClass[sp1].lines
        emotions = {"anticipation":0.0, "fear":0.0, "anger":0.0,"trust":0.0, "surprise":0.0, "sadness":0.0, "joy":0.0, "disgust":0.0}
        first = True
        for num in lineNums:
            if sp2 == "everyone" or sp2 == tp.dialogues[num].recipient:
                p = True
                diag = tp.dialogues[num]
                for e in emotions:
                    if first:
                        emotions[e] = diag.getAverageEmotion(e)
                        first = False
                    else:
                        emotions[e] = (emotions[e] + diag.getAverageEmotion(e)) / 2
        # if not p:
            # print sp1, " never spoke to ", sp2
        return emotions

    """
        Compares the overall sentiment sp1 feels toward sp2.
        Finds all of the lines sp1 says to sp2 and finds the average sentiment scores of sp1 while taking to sp2
        If you type "everyone" as sp2, it will calculate sp1's overall emotion toward the group.
        Returns an array of sentiment scores that sp1 feels while talking to sp2.

    """
    def sentimentAverageBwSpeakers(self, tp, sp1, sp2):
        p = False
        if sp1 == "everyone":
            print "Speaker 1 cannot be everyone"
            return []
        lineNums = tp.speakerToClass[sp1].lines
        sentiment = [0.0,0.0,0.0,0.0]
        first = True
        for num in lineNums:
            if sp2 == "everyone" or sp2 == tp.dialogues[num].recipient:
                p = True
                diag = tp.dialogues[num]
                print diag.sentiment
                for s in range(len(sentiment)):
                    if first:
                        sentiment[s] = diag.sentiment[s]
                        first = False
                    else:
                        sentiment[s] = (sentiment[s] + diag.sentiment[s])/2
        if not p:
            print sp1, " never spoke to ", sp2
        return sentiment

    """
    calculates the overall emotion scores of the converation by averaging all of the average emotion scores between speakers.
    """
    def getConversationScore(self, tp):
        emotions = {"anticipation": 0.0, "fear": 0.0, "anger": 0.0, "trust": 0.0, "surprise": 0.0, "sadness": 0.0,
                    "joy": 0.0, "disgust": 0.0}
        n=0
        for s1 in tp.speakerDict:
            e = self.emotAverageBwSpeakers(tp, s1, "everyone")
            for em in emotions.keys():
                emotions[em] += e[em]
            n += 1
            for s2 in tp.speakerDict:
                 if s1 != s2:
                    e = self.emotAverageBwSpeakers(tp, s1, s2)
                    for em in emotions.keys():
                        emotions[em] += e[em]
                    n +=1

        if n > 0:
            for e in emotions.keys():
                emotions[e] = emotions[e]/n
            return emotions
        else:
            return {}



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
    a.getDummyExample()
    #a.getSentimentOfWords(tp)
    #speakers = tp.speakerDict.keys()
    #di= tp.dialogues
    #a.getEmotionSpeaker(tp, speakers[0], "anticipation")
    #a.lineGraphSentiment(tp, speakers, "joy")
    #e = a.emotAverageBwSpeakers(tp, "Tempus", "Bunnycrusher")
    #s = a.sentimentAverageBwSpeakers(tp, "Tempus", "everyone")
    #a.plotlyEmotionTester(tp, speakers, "joy")
    #print a.getAverageVaderSentimentWords(tp)
    #p = a.getConversationScore(tp)
    #for e in p.keys():
    #    print e, p[e]

    #print s
    #for k in e.keys():
    #    print k, e[k]
    #a.scatterPlotSentiment(tp, speakers, "pos")
    #print speakers[0], a.getAverageEmotionScore(speakers[0], "anticipation")
    #a.plotlyEmotion(tp, speakers,"joy")
    #a.getConversationSentiment(tp)
    #a.setDialogSentiment(tp)
    #a.getTwitterDictSentiment(tp)
    #a.getSentimentTextVader(tp)
    #a.getVaderSentimentWords(tp)
    #print a.getAverageScores(tp)
    #print a.getSentimentData(tp, "Tempus")
    #print a.getConversationSentiment(tp)
    #a.getDifference(tp, ["Tempus", "Bunnycrusher", "Daner"], "pos")
