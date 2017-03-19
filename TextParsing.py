import Dialog
import Person
import nltk
from nltk import word_tokenize
import json
import plotly.plotly as py
import plotly.graph_objs as go

"""
fdist = FreqDist(samples)   ======> create a frequency distribution containing the given samples
fdist[sample] += 1          ======> increment the count for this sample
fdist['monstrous'] 	        ======> count of the number of times a given sample occurred
fdist.freq('monstrous')     ======> frequency of a given sample
fdist.N() 	                ======> total number of samples
fdist.most_common(n) 	    ======> the n most common samples and their frequencies
for sample in fdist: 	    ======> iterate over the samples
fdist.max() 	            ======> sample with the greatest count
fdist.tabulate() 	        ======> tabulate the frequency distribution
fdist.plot() 	            ======> graphical plot of the frequency distribution
fdist.plot(cumulative=True) ======> cumulative plot of the frequency distribution
fdist1 |= fdist2 	        ======> update fdist1 with counts from fdist2
fdist1 < fdist2 	        ======> test if samples in fdist1 occur less frequently than in fdist2
"""

"""
self.dialogues -> a list of Dialog objects that occur in the conversation. These Dialogs are in the order of occurence
self.speakerDict ==> a dictionary that maps speakers to a list of indices into self.dialogs. These corresponds to a speaker's lines in the dialog.
self.speakerText --> a dictionary that maps speakers to a nltk.Text document of their particular lines
self.speakerToClass =-> dictionary that maps the speaker to his or her corresponding class
self.text ==> a nltk text document that represents the entire conversation
"""
class TextParsing:
    def __init__(self, str):
        self.dialogues = []
        self.speakerDict = {}
        self.speakerText = {}
        self.speakerToClass = {}
        self.text = None
        self.freqDist = None
        self.parse(str)

#TODO Complete this method
    def csvparse(self, str):
        fh = open(str, 'r')
        content = fh.readlines()
        for line in content:
            arr = line.split()
            print arr

        fh.close()

    def parse(self, str):
        fh = open(str, 'r')
        content = fh.readlines()
        lines = []
        tokens = []
        for line in content:
            lines.append(line)
        fh.close()
        i = 0
        index = 0
        while (i < len(lines)):
            line = lines[i]

            if line[:4] == '\cf0':
                #print 'entered if'
                i += 2
                line = lines[i]
                timestamp = line[5:]
                timestamp = timestamp[:(len(timestamp)- 7)]

                i += 2
                line = lines[i]
                content = line[5:len(line) - 2]

                i += 4
                line = lines[i]
                date = line[5:(len(line)-7)]

                i += 2
                line = lines[i]
                time = line[5:(len(line) - 7)]

                i += 2
                line = lines[i]
                speaker = line[5:(len(line) - 7)]
                if speaker not in self.speakerDict:
                    self.speakerDict[speaker] = []
                    self.speakerText[speaker] = []
                    self.speakerToClass[speaker] = Person.Person(speaker, self.speakerDict[speaker])

                i += 2
                line = lines[i]
                recipients = line[5:(len(line) - 7)]

                i += 2
                line = lines[i]
                startsAt = line[5:(len(line) - 12)]
                tokens.extend(word_tokenize(content.strip()))
                self.dialogues.append(Dialog.Dialog(timestamp, content, date, time, speaker, recipients, startsAt))
                self.speakerDict[speaker].append(index)
                self.speakerText[speaker].extend(word_tokenize(content.strip()))
                index += 1
                i += 4
            else:
                i += 1
        self.text = nltk.Text(tokens)
        self.freqDist = nltk.FreqDist(self.text)
        for sp in self.speakerText.keys():
            spLines = self.speakerText[sp]
            self.speakerText[sp] = nltk.Text(spLines)
            self.speakerToClass[sp].text = nltk.Text(spLines)
            self.speakerToClass[sp].contribution = len(spLines)/len(tokens)
            self.speakerToClass[sp].freqDist = self.getFrequDistSpeaker(sp)



    """
    returns a frequency distribution nltk object using only the words of a particular speaker particular speaker
    """
    def getFrequDistSpeaker(self, speaker):
        if speaker == "everyone":
            return self.freqDist
        return nltk.FreqDist(self.speakerText[speaker])

    # gets the first n common words that were spoken in the conversation
    # returns a list of tuples. ex: [(',', 176), ('the', 155), ('I', 105), ('you', 89), ('to', 85), ('it', 85), ('we', 82), ('?', 69)]
    def getNCommonWords(self, n):
        return self.freqDist.most_common(n)

    def plotlyBarFreqDist(self, speaker):
        if speaker == "everyone":
            fdist1 = self.freqDist
        else:
            fdist1 = self.getFrequDistSpeaker(speaker)
        xs = []
        ys = []
        for point in fdist1.most_common(50):
            print point
            xs.append(point[0])
            ys.append(point[1])
        # data.append(json.dumps(trace, separators=(',', ':')))
        trace = {"x":xs, "y":ys, "type": "bar"}
        json_data = json.dumps(trace, separators=(",", ":"))
        return json_data

    def plotlyBarFreqDistTest(self, speaker):
        if speaker == "everyone":
            fdist1 = self.freqDist
        else:
            fdist1 = self.getFrequDistSpeaker(speaker)
        xs = []
        ys = []
        print fdist1
        for point in fdist1.most_common(50):
            print point
            xs.append(point[0])
            ys.append(point[1])

    # Concordance tells you all of the times the word is in said in the conversation along with its context
    def getConcordance(self, word):
        return self.text.concordance(word)

    # counts the number of time the word was said in the conversation
    def getFrequecyOfWord(self, word):
        return self.text.count(word)

    #Returns a list of words that only appear once
    def getHapaxes(self):
        return self.freqDist.hapaxes()


if __name__ == '__main__':
    tp = TextParsing("exampleData.rtf")
    tp.plotlyBarFreqDistTest("everyone")
    #print tp.text.concordance('kill')
    #This positional information can be displayed using a dispersion plot.
    # Each stripe represents an instance of a word, and each row represents the entire text.
    #tp.text.dispersion_plot(["kill", "bunny"])

    #print tp.text.count("kill")
    #fdist1 = nltk.FreqDist(tp.text)
    #print tp.speakerText.keys()
    #print tp.getFrequDistSpeaker("Bunnycrusher").most_common(50)
    #gets the first 50 common words that were spoken in the conversation
    #returns a list of tuples. ex: ('Yea', 19)
    #print fdist1.most_common(50)
    #fdist1.plot(50, cumulative=True)
    #Returns a list of words that only appear once
    #print fdist1.hapaxes()
