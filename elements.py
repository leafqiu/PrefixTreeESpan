class GrowthElement:
    def __init__(self, label, n):
        self.label = label
        self.attached = n
    def __eq__(self, other):
        return (self.label == other.label) and (self.attached == other.attached)
    def attached(self):
        return self.attached
    def label(self):
        return self.label

class ProjectedInstance:
    def __init__(self, tid, st, ed, attachposition):
        self.tid = tid
        self.st = st
        self.ed = ed
        self.attachpos = attachposition
    def tid(self):
        return self.tid
    def st(self):
        return self.st
    def ed(self):
        return self.ed
    def attachposition(self):
        return self.attachpos


