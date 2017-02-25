import Dialog
import Person
import nltk
from nltk import word_tokenize
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

class TextParsing:
    def __init__(self, str):
        self.dialogues = []
        self.speakerDict = {}
        self.speakerToClass = {}
        self.text = None
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
                index += 1
                i += 4
            else:
                i += 1
        self.text = nltk.Text(tokens)



if __name__ == '__main__':
    tp = TextParsing("exampleData.rtf")
    #Concordance tells you all of the times the word is in said in the conversation along with its context
    #print tp.text.concordance('kill')
    #This positional information can be displayed using a dispersion plot.
    # Each stripe represents an instance of a word, and each row represents the entire text.
    #tp.text.dispersion_plot(["kill", "bunny"])
    #counts the number of time the word kill was said in the conversation
    #print tp.text.count("kill")
    fdist1 = nltk.FreqDist(tp.text)
    #gets the first 50 commen words that were spoken in the conversation
    #returns a list of tuples. ex: ('Yea', 19)
    #print fdist1.most_common(50)
    #fdist1.plot(50, cumulative=True)
    #Returns a list of words that only appear once
    #print fdist1.hapaxes()
