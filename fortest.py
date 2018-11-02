
import os
input = os.path.join('testdatas', 'D10.data')
with open(input, 'r', encoding='utf-8') as f:
    line = f.readline()
print(line)