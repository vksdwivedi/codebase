import glob
import sys

fileNames = glob.glob("../../Desktop/ssidFiles/20210521*.json")

for file in fileNames:
    with open(file) as f:
        j = f.readlines()
        output = file[:14] + "10LineInputs" + file[23:]
        with open(output, 'w') as k:
            for i in j[:10]:
                k.write(i)