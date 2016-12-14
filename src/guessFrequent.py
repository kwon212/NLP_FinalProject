import autograd.scipy.misc as snp
import autograd.numpy as np
from autograd import grad
import math
import os
from collections import defaultdict, Counter
import random

filefull = "/Users/soyonkwon/nlpfinal/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/responses/tokenized/"
fullFile =  os.listdir(filefull)
tot = len(fullFile)
#print (tot)
train = fullFile[0:math.ceil(tot*0.6)]
dev = fullFile[math.ceil(tot*0.6):math.ceil(tot*0.7)]
test = fullFile[math.ceil(tot*0.9):]
filename = "/Users/soyonkwon/nlpfinal/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/index.csv"

correctLevel = {}
def getCorrectLevel():
    
    mostCommon = []
    with open(filename) as indexfile:
            for line in indexfile:
                    line = line.split(",")
                    mostCommon.append(line[3].strip("\n"))
                    correctLevel[line[0].strip("\n")]=(line[3].strip("\n"))
                    mc = Counter(mostCommon)
            print(mc, mc.most_common(1))
            return mc.most_common(1)

cl = getCorrectLevel()
cor = 0
incor = 0
for t in test:

    if  correctLevel.get(t) == cl:
        cor +=1
    incor +=1


print (cor/incor)