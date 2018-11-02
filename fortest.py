import os

if __name__ == '__main__':
    testnames = 'testdatas'
    inputs = [os.path.join('./', testnames, name) for name in ['F5.data', 'D10.data']]
    sup = [100, 1000, 10000]
    outnames = 'outputs'
    for name in inputs:
        for s in sup:
            out = os.path.basename(name).split('.')[0] + '-' + str(s) + '.out'
            output = os.path.join('./', outnames, out)
            os.system("python ./prefixtreeespan.py -i %s -o %s -s %d" % (name, output, s))
