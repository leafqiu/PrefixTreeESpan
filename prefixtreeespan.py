import getopt
import sys, os, math

from elements import ProjectedInstance, GrowthElement
from tree import OriginalTree, SubtreePattern


def getargs():
    global inputfile
    inputfile = os.path.join('testdatas', 'D10.data')
    global outputfile
    outputfile = os.path.join('outputs', 'output.data')
    global min_sup
    min_sup = 0.003
    if len(sys.argv) == 0:
        return
    try:
        opts, args = getopt.getopt(sys.argv, "i:o:s:")
    except getopt.GetoptError:
        print('usage: python prefixtreeespan.py -i <inputfile> -o <outputfile> -s <min_sup>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            global inputfile
            inputfile = arg
        elif opt == '-o':
            global outputfile
            outputfile = arg
        elif opt == '-s':
            global min_sup
            min_sup = float(arg) / 100  # 0.3%
def readtrees():
    trees = []
    with open(inputfile, 'rt', encoding='utf-8') as f:
        index = 0
        for line in f:
            nodes = line.strip().split(' ')
            tree = OriginalTree(index, nodes)
            trees.append(tree)
            index += 1
    return trees
def prodbfromdb(trees, label):
    prodb = []
    for tree in trees:
        for index, node in enumerate(tree.nodes()):
            if node == label:
                partner = tree.partnerindex(index)
                if (index + 1) < partner: # leaf label has no proinstance
                    proinstance = ProjectedInstance(tree.id(), index + 1, partner, 1)
                    prodb.append(proinstance)
    return prodb
def frequentpattern(trees, subtree, prodb):
    # find all frequent growth element
    growthele = {}
    for proins in prodb:
        tree = trees[proins.tid()]
        for node in tree.nodes()[proins.st(): proins.ed()]:
            if node != '-1':
                ge = GrowthElement(node, proins.attachposition())
                if growthele.__contains__(ge):
                    growthele[ge] += 1
                else:
                    growthele[ge] = 1
    freges = []
    for ge, sup in growthele.items():
        global min_sup
        if sup >= min_sup:
            freges.append(ge)
    # for each growth-element, extend subtree to (subtree + 1)
    for ge in freges:
        # extend subtree with ge and write it
        pattern = SubtreePattern(subtree, ge)
        with open(outputfile, 'a', encoding='utf-8') as f:
            for node in pattern.nodes():
                f.write(node + ' ')
            f.write('\n')
        # find all occurrences of ge and construct (subtree + 1)'s projected database
        label = ge.label()
        newprodb = []
        for proins in prodb:
            tree = trees[proins.tid()]
            treenodes = tree.nodes()
            for index, node in enumerate(treenodes[proins.st(): proins.ed()], proins.st()):
                # find occurrence
                if node == label:
                    partnerindex = tree.partnerindex(index)
                    # new position vs. occurrence's attached position
                    prestind = index
                    poststind = partnerindex
                    for subindex, subnode in enumerate(treenodes[(index + 1): partnerindex]):
                        if subnode != '-1':
                            prestind = subindex
                            break
                    for subindex, subnode in enumerate(treenodes[(partnerindex + 1): proins.ed()]):
                        if subnode != '-1':
                            poststind = subindex
                            break
                    # construct projected instance
                    if prestind > index and prestind < partnerindex:
                        newproins = ProjectedInstance(proins.tid(), prestind, partnerindex, pattern.lastposition())
                        newprodb.append(newproins)
                    if poststind > partnerindex:
                        newproins = ProjectedInstance(proins.tid(), poststind, proins.ed(), proins.attachposition())
                        newprodb.append(newproins)
        frequentpattern(trees, pattern, newprodb)

def prefixtreeespan(trees):
    # find all frequent label b: length-1 pattern
    labels = {}
    frequent_labels = []
    for tree in trees:
        for node in tree.nodes():
            if node != '-1':
                if labels.__contains__(node):
                    labels[node] += 1
                else:
                    labels[node] = 1
    for key, value in labels.items():
        global min_sup
        if value >= min_sup:
            frequent_labels.append(key)

    for label in frequent_labels:
        nodes = [label, '-1']
        len1subtree = SubtreePattern(None, nodes)
        # output pattern tree <b -1>
        with open(outputfile, 'a', encoding='utf-8') as f:
            for node in len1subtree.nodes():
                f.write(node + ' ')
            f.write('\n')
        # constrcut <b -1> projected database
        prodb = prodbfromdb(trees, label)
        #  grow pattern's length by growth element
        frequentpattern(trees, len1subtree, prodb)

if __name__ == '__main__':
    getargs()
    trees = readtrees()
    global min_sup
    min_sup = math.ceil(min_sup * len(trees))
    prefixtreeespan(trees)