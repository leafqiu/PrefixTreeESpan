import datetime
import getopt
import sys, os, math

from elements import ProjectedInstance, GrowthElement
from tree import OriginalTree, SubtreePattern


def getargs():
    global inputfile
    inputfile = os.path.join('testdatas', 'testin.data')
    global outputfile
    outputfile = os.path.join('outputs', 'testout.out')
    global min_sup
    min_sup = 2
    if len(sys.argv) == 0:
        return
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:s:")
    except getopt.GetoptError:
        print('usage: python prefixtreeespan.py -i <inputfile> -o <outputfile> -s <min_sup>')
        sys.exit(2)
    # print(opts)
    for opt, arg in opts:
        if opt == '-i':
            inputfile = arg
        elif opt == '-o':
            outputfile = arg
        elif opt == '-s':
            min_sup = int(arg)
    if os.path.exists(outputfile):
        os.remove(outputfile)
    # print(inputfile, outputfile, min_sup)


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
                    proinstance = ProjectedInstance(tree.tid, index + 1, partner, 0)
                    prodb.append(proinstance)
    return prodb


def frequentpattern(trees, subtree, prodb):
    # find all frequent growth element
    growthele = {}
    for proins in prodb:
        tree = trees[proins.tid]
        for node in tree.nodes()[proins.st: proins.ed]:
            if node != '-1':
                ge = GrowthElement(node, proins.attachindex)
                if ge not in growthele:
                    growthele[ge] = set([])
                growthele[ge].add(tree.tid)
    global min_sup
    freges = [ge for ge, idset in growthele.items() if len(idset) >= min_sup]
    # for each growth-element
    for ge in freges:
        # extend subtree with ge and write it
        pattern = SubtreePattern(subtree, ge)
        output(pattern.nodes())
        # find all occurrences of ge and construct (subtree + 1)'s projected database
        # one occurrence corresponding to one projected instance
        newprodb = []
        for proins in prodb:
            tree = trees[proins.tid]
            treenodes = tree.nodes()
            for index, node in enumerate(treenodes[proins.st: proins.ed], proins.st):
                # find occurrence
                if node == ge.label and ge.attached == proins.attachindex:
                    partnerindex = tree.partnerindex(index)
                    prestind = index
                    poststind = partnerindex
                    for subindex, subnode in enumerate(treenodes[(index + 1): partnerindex], (index + 1)):
                        if subnode != '-1':
                            prestind = subindex
                            break
                    for subindex, subnode in enumerate(treenodes[(partnerindex + 1): proins.ed], (partnerindex + 1)):
                        if subnode != '-1':
                            poststind = subindex
                            break
                    # if pattern.nodes()[0] == 'A' and pattern.nodes()[1] == 'B':
                    #     print(proins.tid, index, partnerindex, prestind, poststind)

                    # construct projected instance
                    if index < prestind < partnerindex:
                        # hanging on the last node
                        newproins = ProjectedInstance(proins.tid, prestind, partnerindex, pattern.lastindex)
                        newprodb.append(newproins)
                        # hanging on the ancestors of last node
                        patnodes = pattern.nodes()
                        stindex = pattern.partnerof(pattern.lastindex) + 1
                        edindex = len(patnodes)
                        for patindex in range(stindex, edindex):
                            if patnodes[patindex] == '-1' and pattern.partnerof(patindex) < pattern.lastindex:
                                newproins = ProjectedInstance(proins.tid, prestind, partnerindex, pattern.partnerof(patindex))
                                newprodb.append(newproins)
                    if poststind > partnerindex:
                        newproins = ProjectedInstance(proins.tid, poststind, proins.ed, proins.attachindex)
                        newprodb.append(newproins)

        frequentpattern(trees, pattern, newprodb)


def output(nodes):
    global outputfile
    with open(outputfile, 'a', encoding='utf-8') as f:
        s = ' '.join(nodes)
        f.write(s + ' \n')


def prefixtreeespan(trees):
    # find all frequent label b: length-1 pattern
    # frequency: hwo many trees this label occurs in
    labels = {}
    for tree in trees:
        for node in tree.nodes():
            if node != '-1':
                if node not in labels:
                    labels[node] = set([])
                labels[node].add(tree.tid)
    # for label, idset in labels.items():
    #     print(label, len(idset))
    global min_sup
    frequent_labels = [label for label, idset in labels.items() if len(idset) >= min_sup]
    for label in frequent_labels:
        nodes = [label, '-1']
        len1subtree = SubtreePattern(None, nodes)
        # output pattern tree <b -1>
        output(len1subtree.nodes())
        # constrcut <b -1> projected database
        prodb = prodbfromdb(trees, label)
        # if label == 'A':
        #     for ii in prodb:
        #         print(ii)

        #  grow pattern's length by growth element
        frequentpattern(trees, len1subtree, prodb)


if __name__ == '__main__':
    getargs()
    time_start = datetime.datetime.now()
    trees = readtrees()
    # for tree in trees:
    #     print(tree.pre_order_string)
    #     print(tree.partner)
    # print(len(trees))
    prefixtreeespan(trees)
    time_end = datetime.datetime.now()
    with open(outputfile, 'a', encoding='utf-8') as f:
        f.write('Time used: ' + str(time_end - time_start) + '\n')
