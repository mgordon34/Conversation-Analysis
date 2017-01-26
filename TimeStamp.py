class TimeStamp:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def duration(self):
        return self.start - self.end


