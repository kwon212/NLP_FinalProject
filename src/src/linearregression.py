
from sklearn import linear_model
from lregression import LogisticRegression
from ckyParser import ParseTree
import os
import math
import pandas as pd

clf = linear_model.LinearRegression()

filefull = "/Users/soyonkwon/nlpfinal/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/responses/tokenized/"
fullFile =  os.listdir(filefull)
tot = len(fullFile)
#print (tot)
train = fullFile[0:math.ceil(tot*0.6)]
dev = fullFile[math.ceil(tot*0.6):math.ceil(tot*0.7)]
test = fullFile[math.ceil(tot*0.9):]
filename = "/Users/soyonkwon/nlpfinal/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/index.csv"

l = LogisticRegression()
l.getCorrectLevel()
l.trainModel(train)
rl = l.runModel(train)

# p = ParseTree()
# p.readTree("hw4-data/train.trees.pre.unk")
# p.getcProb()
# pl = p.viterbiCky()

#data structures to store train, test probs
rll = list()
rlm = list()
rlh = list()
rll1 = list()
rlm1 = list()
rlh1 = list()

for r in rl:
    rll.append(r.get("low"))
    rlm.append(r.get("medium"))
    rlh.append(r.get("high"))


correctLevel = dict()

def getMaxLength(file):
        maxLength = 0
        mList = list()
        for name in file:
    #print (name)
            with open(filefull + name) as f:
                for line in f:
                        line = line.split()
                        for word in line:

                                if len(word) > maxLength:
                                        if len(word)< 40:
                                        #       print (word)


                                                maxLength = len(word)
                mList.append(maxLength)
        return mList

def getSentenceLength(file):
        max = 0
        mList = list()
        for name in file:
    #print (name)
            with open(filefull + name) as f:
                for line in f:
                        line = line.split()
        #               print (line)
                        #print len(line)
                        if len(line) > max:
                                max = len(line)

                mList.append(max)
        return mList

def getCorrectLevel():
    #correctLevel = {}
    with open(filename) as indexfile:
                for line in indexfile:
                #for line in f:
   # with open(filename) as indexfile:
    #        for line in indexfile:
                    line = line.split(",")
                    #mostCommon.append(line[3].strip("\n"))
                    correctLevel[line[0].strip("\n")]=(line[3].strip("\n"))
                    #mc = Counter(mostCommon)



def getcorrectList(file):
    cl = list()
    for name in file:
        if correctLevel.get(name) == "low":
            cl.append(0)
        elif correctLevel.get(name) == "medium":
            cl.append(10)
        else:
            cl.append(20)
    return cl

getCorrectLevel()    
cl = getcorrectList(train)
#print (len(cl), len(rlh))

wList = getMaxLength(train)

sList = getSentenceLength(train)

newPD = pd.DataFrame( {"cl" : cl, "wList": wList, "sList": sList, "rlm": rlm, "rlh": rlh, "rll": rll })
X= newPD.drop('cl', axis = 1)

clf.fit(X, newPD.cl)
print (clf.intercept_)
print (clf.coef_, X.columns)

l1 = LogisticRegression()
l1.getCorrectLevel()
l1.trainModel(test)
rl1 = l1.runModel(test)

for r in rl1:
    rll1.append(r.get("low"))
    rlm1.append(r.get("medium"))
    rlh1.append(r.get("high"))

cl1 = getcorrectList(test)

sList1 = getSentenceLength(test)
wList1 = getMaxLength(test)
print (len(rll1), len(cl1), len(sList1), len(wList1))

#print (pd.DataFrame(zip(X.columns, clf.coef_), columns -['features', 'coef']))
cor = 0
incor = 0
for i in range(len(sList1)):
    predictedLevel = 15.2022721559-0.3844683*wList1[i]+0.02033061*sList1[i]+0.98008422 *rlm1[i]+0.00396789 *rll1[i]-0.00166023*rlh1[i]
   # print (predictedLevel)
    if predictedLevel <= 5:
        predictedLevel = 0
    elif predictedLevel <= 15:
        predictedLevel = 10
    else:
        predictedLevel = 20
    if predictedLevel == cl1[i]:
        cor += 1
    incor += 1
print (cor, incor, cor/incor)    
#clf.fit([wList,sList, rll, rlm] , cl)

