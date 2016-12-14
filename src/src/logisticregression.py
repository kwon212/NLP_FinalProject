#l project
#So Yon Kwon

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

class LogisticRegression:
    def __init__(self):
        self.level = ["low", "medium", "high"]

        self.eta = 0.08
        self.C=0.3
        self.uniqueWords = list()
        self.wordWeight = np.zeros((1,1))
        self.correctLevel = dict()

    def getCorrectLevel(self):
        #correctLevel = {}
        mostCommon = []        
        with open(filename) as indexfile:
                for line in indexfile:
                        line = line.split(",")
                        mostCommon.append(line[3].strip("\n"))
                        self.correctLevel[line[0].strip("\n")]=(line[3].strip("\n"))
                        mc = Counter(mostCommon)
                #print(mc, mc.most_common(1))
                #return self.correctLevel
        
    def trainModel(self, train):
        for name in train:
    #print (name)
            with open(filefull + name) as f:
                #rint (name)
                for line in f:
                    line = line.split(' ')
                    line.append("<bias>")
                    for word in line:
                        if word not in self.uniqueWords:
                            self.uniqueWords.append(word)
                # prev = line[0]
                # for word in line[1:]:
                #     bigram = prev + " " + word
                #     if bigram not in self.uniqueWords:
                #         self.uniqueWords.append(bigram)
                # prev = word
                self.wordWeight = np.zeros((len(self.level), len(self.uniqueWords)))
                #print (self.correctLevel)

    def getlogProb(self,model, doc, pl,unique, level):
        line  = doc.split(' ')
        #line.pop(0)
        line.append("<bias>")
        wordCol = [] 
        prob = 0
        denominator = 0
        numerator = 0
            
        for word in line:
            if word in unique:

                if unique.index(word) not in wordCol:
                    wordCol.append(unique.index(word))
     
        # prev = line[0]
        # for word in line[1:]:
        #     bigram = prev + " " + word
        #     if bigram in self.uniqueWords:
        #         if self.uniqueWords.index(bigram) not in wordCol:
        #             wordCol.append(self.uniqueWords.index(bigram))
        #     prev = word

    #@#sum2 = 0

        sum2 = 0
        for p in self.level:
            sum2 += np.exp(np.sum(model[level.index(p), wordCol]))
        denominator = np.log(sum2)            
        numerator = np.sum(model[level.index(pl),wordCol]) #P(K|d) for pres
        prob =  denominator - numerator

        return prob




    def getAccuracy(self, wordWeight, line, printTrue, name): 
        first = 0
        guessDev= dict()
        rList = []
        doc = line.rstrip().split(",")
        right = self.correctLevel.get(name)
        for p in self.level:
            
            guessDev[p]= np.exp(self.getlogProb(wordWeight, line, p, self.uniqueWords, self.level))

  
        guesssLevel = min (guessDev, key=guessDev.get)
        return guessDev
        #print (guessLevel, right)
        #if right == guesssLevel:
        #    return 1
        #return 0

    def runModel(self, train):
        for i in range(15):
            sumz = 0
            cor = 0
            incor = 0
            guesDev = []
            random.shuffle(train)
            for name in train:
                with open(filefull + name) as f:
                    for line in f:
                        sum1 = 0

                        words = line.rstrip().split()

                        pl = self.correctLevel.get(name)
                        words = line[1:]
            
                
                        gradnew = grad(self.getlogProb)
                        self.wordWeight -= self.eta * gradnew(self.wordWeight, line, pl, self.uniqueWords, self.level)

                        sumz += self.getlogProb(self.wordWeight, line, pl, self.uniqueWords, self.level)
       
                        first = 0


            rList = list()
            for n in train:
                with open(filefull + n) as f:
                    for line in f:
                        line += " " + line                           
                    rList.append(self.getAccuracy(self.wordWeight, line, 0, n))


            return (rList)
                        






