import sys
import os
from collections import defaultdict, Counter
from random import shuffle
def getCorrectAge(filename):
	correctAge = {}
	mostCommon = []
	with open(filename) as indexfile:
		for line in indexfile:
			line = line.split(",")
			mostCommon.append(line[3].strip("\n"))
			correctAge[line[0].strip("\n")]=(line[3].strip("\n"))
			mc = Counter(mostCommon)
		print(mc, mc.most_common(1))
		return correctAge   
		 
def findMaxWdLength(tokens):
	maxWdLength = 0

	for token in tokens:
		word = token.split('/')[0]
		if word != 'USER' and len(word) > maxWdLength:
			maxWdLength = len(word)

	return maxWdLength


def getMaxLength(filename):
        maxLength = 0
        with open(filename) as f:
                for line in f:
                        line = line.split()
                        for word in line:
	
				if len(word) > maxLength:
					if len(word)< 40:
					#	print (word)


						maxLength = len(word)
	return maxLength


def getSentenceLength(filename):
	max = 0
	with open(filename) as f:	
		for line in f:
			line = line.split()
	#		print (line)
			#print len(line)
			if len(line) > max:
				max = len(line)
	return max

def predictLevel(filefull, correctLevel):
	docs = 0
	correct = 0

	low = 0
	medium = 0
	high = 0
	i = 0

	absMax = dict()
	absMax["low"] = 0
	absMax["medium"] = 0
	absMax["high"] = 0
	absSen = dict()
	absSen["low"] = 0
        absSen["medium"	] = 0
        absSen["high"] = 0

	trainNum = len(os.listdir(filefull))*0.7
	devNum = len(os.listdir(filefull))*0.85
	#print (trainNum)
	x = os.listdir(filefull)
	#shuffle(x)
	#print (x)
	for filename in x:
		'''
		if trainNum > i:	
			maxLength = getMaxLength(filefull + filename)
			senLength = getSentenceLength(filefull + filename)
			if maxLength > absMax[correctLevel.get(filename)]:
				absMax[correctLevel.get(filename)] = maxLength
				
			if senLength > absSen[correctLevel.get(filename)]:
				absSen[correctLevel.get(filename)] = senLength
	#	print (absMax, absSen)
		if i > trainNum and i < devNum:	
			wlength = getMaxLength(filefull + filename)
                        slength = getSentenceLength(filefull + filename)
			if wlength < absMax["low"] or slength < absSen["low"]:
		                age =  "low"
       			elif wlength < absMax["medium"] or slength < absSen["medium"]:
                		age = "medium"
        		else:
                		age = "high"

		  '''
		if i > trainNum and i < devNum:
			if "medium" == correctLevel.get(filename):
				print (correctLevel.get(filename))
				correct += 1
			docs += 1
		
		i += 1
			#t += 1
			#print (i)
	#print (len(correctLevel), len(os.listdir(filefull)))
	return correct / float(docs)


if __name__ == "__main__":
	filefull = "/afs/crc.nd.edu/group/nlp/02/dchiang/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/responses/tokenized/"
		
	correctAge = getCorrectAge("/afs/crc.nd.edu/group/nlp/02/dchiang/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/index.csv")	
	print predictLevel(filefull, correctAge)
	print correctAge.get("1190625.txt")

