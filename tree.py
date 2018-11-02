
class OriginalTree:
    def __init__(self, id, nodes):
        self.tid = id
        self.pre_order_string = []
        self.pre_order_string.extend(nodes)
        self.partner = []
        self.buildtree()
    def buildtree(self):
        stack = []
        for index in range(len(self.pre_order_string)):
            if self.pre_order_string[index] == '-1':
                first = stack.pop()
                self.partner.insert(first, index)
                self.partner.insert(index, first)
            else:
                stack.append(index)
    def id(self):
        return self.tid
    def nodes(self):
        return self.pre_order_string
    def partnerindex(self, index):
        return self.partner[index]

class SubtreePattern:
    def __init__(self, subtree, ge):
        self.pre_order_string = []
        self.lastposition = 0
        self.position = []
        self.partner = []
        if subtree == None: # ge is a list of nodes
            self.pre_order_string.extend(ge)
        else:   # ge is growth element
            newnodes = [ge.label(), '-1']
            attachedind = subtree.nodein(ge.attached())
            insertpos = subtree.partnerof(attachedind)
            self.pre_order_string = subtree.nodes()[0:insertpos].extend(newnodes).extend(subtree.nodes()[insertpos:])
        self.buildtree()
    def buildtree(self):
        stack = []
        curposition = 1
        for index in range(len(self.pre_order_string)):
            if self.pre_order_string[index] == '-1':
                first = stack.pop()
                self.partner.insert(first, index)
                self.partner.insert(index, first)
            else:
                stack.append(index)
                self.position.insert(curposition, index)
                curposition += 1
        self.lastposition = curposition - 1
    def nodes(self):
        return self.pre_order_string
    def nodein(self, pos):
        return self.position[pos]
    def partnerof(self, index):
        return self.partner[index]
    def lastposition(self):
        return self.lastposition