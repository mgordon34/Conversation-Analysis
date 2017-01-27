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
        if line[:4] == '\cf0':
            i += 2
            line = lines[i]
            timestamp = line[5:]
            timestamp = timestamp[:(len(timestamp)- 7)]
            i += 2
            line = lines[i]
            content = line[6:len(line) - 2]
            i += 4
            line = lines[i]
            date = line[5:(len(line)-7)]
            i += 2
            line = lines[i]
            time = line[5:(len(line) - 7)]
            i += 2
            line = lines[i]
            speaker = line[5:(len(line) - 7)]
            i += 2
            line = lines[i]
            recipients = line[5:(len(line) - 7)]
            i += 2
            line = lines[i]
            # if line is "\cf0 \cell \lastrow\\row":
            #     #print 'last row'
            #     startsAt = line[5:(len(line) - 20)]
            #     dialogues.append(Dialog.Dialog(timestamp, content, date, time, speaker, recipients, startsAt))
            #     i += 4
            # else:
            startsAt = line[5:(len(line) - 12)]
            dialogues.append(Dialog.Dialog(timestamp, content, date, time, speaker, recipients, startsAt))
            i += 4
        else:
            i += 1
    return dialogues