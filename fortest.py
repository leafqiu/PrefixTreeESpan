import math
import os

if __name__ == '__main__':
    testnames = 'testdatas'
    inputs = [os.path.join(testnames, name) for name in ['F5.data', 'D10.data']]
    sup = [0.3, 0.7, 1, 5, 10]
    len = 100000
    # input = os.path.join(testnames, 'CSlog.data')
    # len = 59691
    # sup = [3.5, 3, 2.5, 2, 1.75, 1.7, 1.65, 1.6, 1.55, 1.5]
    # input = os.path.join(testnames, 'T1M.data')
    # file = open(input,'r',encoding='utf-8')
    # len = len(file.readlines())   # len = 1000000
    # file.close()
    # sup = [0.8, 0.6, 0.4, 0.2, 0.1]
    outnames = 'outputs'
    for input in inputs:
        for s in sup:
            print('mining ' + str(s) + '%...')
            min_sup = math.ceil(len * s / 100)
            out = os.path.basename(input).split('.')[0] + '-' + str(s) + '.out'
            output = os.path.join(outnames, out)
            os.system("python ./prefixtreeespan.py -i %s -o %s -s %d" % (input, output, min_sup))
            # print("python ./prefixtreeespan.py -i %s -o %s -s %d" % (input, output, min_sup))
