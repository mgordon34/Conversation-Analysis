import Dialog


def parse(str):
    dialogues = []
    fh = open(str.name, 'r')
    content = fh.readlines()
    lines = []
    for line in content:
        lines.append(line)
    fh.close()
    i = 0
    while (i < len(lines)):
        line = lines[i]
        # For some reason these strings are not equal when they, in fact, are. THEY ARE PYTHON
        # I have tried everythingprint startsAt from checking if these were unicode or normal python strings (they are both normal)
        # I can quickly switch to the txt file if need be, but I went ahead and coded for a rtf
        if line[:4] == '\cf0':
            print 'entered if'
            i += 2
            line = lines[i]
            timestamp = line[5:]
            timestamp = timestamp[:(len(timestamp)- 7)]
            print timestamp
            i += 2
            line = lines[i]
            content = line[5:len(line) - 2]
            print content
            i += 4
            line = lines[i]
            date = line[5:(len(line)-7)]
            print date
            i += 2
            line = lines[i]
            time = line[5:(len(line) - 7)]
            print time
            i += 2
            line = lines[i]
            speaker = line[5:(len(line) - 7)]
            print speaker
            i += 2
            line = lines[i]
            recipients = line[5:(len(line) - 7)]
            print recipients
            i += 2
            line = lines[i]
            # if line is "\cf0 \cell \lastrow\\row":
            #     #print 'last row'
            #     startsAt = line[5:(len(line) - 20)]
            #     dialogues.append(Dialog.Dialog(timestamp, content, date, time, speaker, recipients, startsAt))
            #     i += 4
            # else:
            startsAt = line[5:(len(line) - 12)]
            print startsAt
            dialogues.append(Dialog.Dialog(timestamp, content, date, time, speaker, recipients, startsAt))
            i += 4
        else:
            i += 1
    print 'end\n'