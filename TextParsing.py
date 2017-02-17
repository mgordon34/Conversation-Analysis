import Dialog
import Person
class TextParsing:
    def __init__(self, str):
        self.dialogues = []
        self.speakerDict = {}
        self.speakerToClass = {}
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

                self.dialogues.append(Dialog.Dialog(timestamp, content, date, time, speaker, recipients, startsAt))
                self.speakerDict[speaker].append(index)
                index += 1
                i += 4
            else:
                i += 1

