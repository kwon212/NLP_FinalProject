#So Yon Kwon
from tree import Tree
from collections import defaultdict, Counter
import math
import time
import matplotlib.pyplot as plot
import numpy as np 
import os 

filefull = "/Users/soyonkwon/nlpfinal/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/responses/tokenized/"
fullFile =  os.listdir(filefull)
tot = len(fullFile)
#print (tot)
train = fullFile[0:math.ceil(tot*0.6)]
dev = fullFile[math.ceil(tot*0.6):math.ceil(tot*0.7)]
test = fullFile[math.ceil(tot*0.9):]
filename = "/Users/soyonkwon/nlpfinal/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/index.csv"

class ParseTree:
    def __init__(self):
        self.rulesList = []
        self.rules = defaultdict(lambda:defaultdict(int))
        self.prob = {}
        self.cntRules = {}
        self.terminals = defaultdict(lambda:set())
        self.probDict = {}  
        self.unaryRules = defaultdict(int)
        self.binaryRules = defaultdict(int)  
        self.uniqueNT = set()
        self.best = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
        self.back = defaultdict(lambda:defaultdict(lambda:defaultdict(list)))
        self.plotTime = []
        self.plotLen = []

    def readTree(self, file):
        with open(file) as f:
            for line in f:
                t = Tree.from_str(line)
                for n in t.bottomup():
                    right = ''
                    for child in n.children:
                        if len(n.children) == 1:

                            self.terminals[child.label.strip()].add(n.label.strip())
                        right = right + ' ' + child.label
                    if right != '':
                        self.rulesList.append( n.label.strip() + " -> " + right.strip())
                        #print (right, len(right.split()))
                        #if len(right.split()) > 1:
                        #    self.binaryRules[(n.label, right.split()[0], right.split()[1])] += 1
                        ##else:
                        #    self.unaryRules[(n.label,right)] += 1     

                        self.rules[n.label.strip()][right.strip()] += 1  
                        self.uniqueNT.add(n.label)
                    #else:
                        #rules[
        self.cntRules = Counter(self.rulesList)
        #print (self.back[1][1][1])
        #self.best[1][1][1]+=1
        #print (self.back[1][1][1], self.best[1][1][1])

    def getcProb(self):
        #robDict = {}
        for rl in self.rules:
                totSum = 0
                for r in self.rules[rl.strip()]:
                    totSum = sum([x for x in self.rules[rl.strip()].values()])
                for r in self.rules[rl.strip()]:
                    if totSum!=0:
                        self.probDict[rl.strip() + ' -> ' + r.strip() ] = float(self.rules[rl.strip()][r.strip()]/totSum)



    def viterbiCky(self):
        ##plotTime = []
        ##plotLen = []
        rList = list()
        for name in train:
    #print (name)
            with open(filefull + name) as f:
                #rint (name)
                totL = 0
                for line in f:
                    a = time.time()
                    words = line.split()
            
                    self.best = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda: 0)))
                    self.back = defaultdict(lambda:defaultdict(lambda:defaultdict(list)))
                  
                    for x in range(0, len(words)): 

                        if words[x] in self.terminals:
                            word = words[x].strip()

                        else:
                            word = '<unk>'


                        for left in self.terminals[word]:

                            if self.probDict[left.strip() + ' -> ' + word.strip()] > self.best[x][x+1][left.strip()]:

                                self.back[x][x+1][left.strip()].append(word.strip())
                                self.best[x][x+1][left.strip()] = self.probDict[left.strip() + ' -> ' + word.strip()]
                                
                               # if (word =="serve"):    
                                #    print (x)

                    for x in range(0, len(words) + 1): 
                        for y in range(0, len(words) + 1 ): 

                            for q in range(y+1, x+y): 
                                for rule in self.rules:
                                    rule = rule.strip()

                                    for right in self.rules[rule]:
                                        rsp = right.split()
                                        if len(rsp) > 1:
                   
                                            if self.probDict[rule.strip() + ' -> ' + right.strip()] * self.best[y][q][rsp[0]] * self.best[q][x+y][rsp[1]] > self.best[y][x+y][rule]:
                                                self.best[y][x+y][rule] = self.probDict[rule.strip() + ' -> ' + right.strip()] * self.best[y][q][rsp[0]] * self.best[q][x+y][rsp[1]]                                    
                                                self.back[y][y+x][rule] =[]
                                                self.back[y][x+y][rule].extend((rsp[0],rsp[1],q))
                                                
                    b = time.time()

                    if self.best[0][len(words)]['TOP'] == 0:
                        print (0)
                        #rList.append(0)
                    else:
                        print (1)
                        totL += math.log(self.best[0][len(words)]['TOP'])/len(words)
                        #rList.append(math.log(self.best[0][len(words)]['TOP'])/len(words))
                rList.append(totL)
        return rList

    def plotGraph(self):
        plot.scatter(np.array(self.plotLen), np.array(self.plotTime))
        plot.show()
        #bFit = np.polyfit(np.array(self.plotLen), np.array(self.plotTime),1)
        #print (bFit[0])

    def getTree(self, r, x, y):

        if len(self.back[x][y][r]) ==1 :
            print("("+r+" " + self.back[x][y][r][0] + ')',end ='')

        else:
            print('(' +r + " " , end = '')
            self.getTree(self.back[x][y][r][0], x, self.back[x][y][r][2])
            print(' ', end = '')
            self.getTree(self.back[x][y][r][1], self.back[x][y][r][2], y)
            print(')', end = '')

