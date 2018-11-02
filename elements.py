class GrowthElement:
    def __init__(self, label, n):
        self.label = label
        self.attached = n

    def __eq__(self, other):
        return (self.label == other.label) and (self.attached == other.attached)

    def __hash__(self):
        return hash(self.label)

    def __str__(self):
        return "GE: (%s, %s)" % (self.label, self.attached)


class ProjectedInstance:
    def __init__(self, tid, st, ed, attachposition):
        self.tid = tid
        self.st = st
        self.ed = ed
        self.attachpos = attachposition

    def __str__(self):
        return "ProIns: (%d, %d, %d, %d)" % (self.tid, self.st, self.ed, self.attachpos)

