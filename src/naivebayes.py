import math
import os 

filefull = "/Users/soyonkwon/nlpfinal/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/responses/tokenized/"
fullFile =  os.listdir(filefull)
tot = len(fullFile)
#print (tot)
train = fullFile[0:math.ceil(tot*0.6)]
dev = fullFile[math.ceil(tot*0.6):math.ceil(tot*0.7)]
test = fullFile[math.ceil(tot*0.9):]
filename = "/Users/soyonkwon/nlpfinal/for_alli/ETS_Corpus_of_Non-Native_Written_English/data/text/index.csv"

totalDocCount = 0

levels = ["low", "medium", "high"]


wordCount = dict()
levelDocCount = dict()
levelWordCount = dict()
wordProb = dict()
vocabulary = set()

correctLevel = dict()
#d = 3 #delta for smoothing
def getCorrectLevel():
        #correctLevel = {}
        #mostCommon = []        
        with open(filename) as indexfile:
                for line in indexfile:
                        line = line.split(",")
                        #mostCommon.append(line[3].strip("\n"))
                        correctLevel[line[0].strip("\n")]=(line[3].strip("\n"))
                        #mc = Counter(mostCommon)
                #print(mc, mc.most_common(1))
                #return self.correctLevel
getCorrectLevel()

for p in levels:
	levelDocCount[p] = 0
	levelWordCount[p] = 0
	wordCount[p] = dict()
	wordProb[p] = dict()


for name in train:
    #print (name)
	with open(filefull + name) as f:
		for line in f:
			line += " " + line
		words = line.rstrip().split()
		level = correctLevel.get(name)
		#level = words[0]
		#words = words[1:]
		#tagBigram = ["<s>"]
		#for w in words:
		#	tagBigram.append(w)
		#tagBigram.append("</s>")
		
		levelDocCount[level] += 1

		for w in words:
			if w not in wordCount[level]:
				wordCount[level][w] = 1
			else:
				wordCount[level][w] += 1

			levelWordCount[level] += 1		
			vocabulary.add(w)

			# previous = " "
			# if len(words) > 0:
			# 	previous = tagBigram[0]
			# 	for w in tagBigram[1:]:
			# 		bigram = previous + " " + w
			# 		#print (bigram)
			# 		if bigram not in wordCount[level]:
			# 			wordCount[level][bigram] = 1
			# 		else:
			# 			wordCount[level][bigram] += 1
			# 		levelWordCount[level] += 1
			# 		vocabulary.add(bigram)
			# 		previous = w


vocabularySize = len(vocabulary)
levelProb = dict()
unkProb = dict()
totalDocCount = len(train)
for p in levels:
	unkProb[p] = 0.09 /(levelWordCount[p] + vocabularySize*0.09 )
	levelProb[p] = levelDocCount[p]/totalDocCount
	for w in wordCount[p]:
		wordProb[p][w] = (float(wordCount[p][w])+0.09)/(levelWordCount[p]+vocabularySize*0.09)

#orrectLevel = dict()


def guess(words):
	#print ("theesee", words)
	allLogProb = dict()
	# tagBigram = ["<s>"]
	# for w in words:
	# 	tagBigram.append(w)
	# tagBigram.append("</s>")
	#words = tagBigram
	for p in levels:
		allLogProb[p] = 0
		for w in words:
			if w in wordProb[p]:
				prob = wordProb[p][w]
			else: #unk
				prob = unkProb[p]
			allLogProb[p] += math.log10(prob)

	
	getSum = allLogProb[levels[0]]
	for p in levels[1:]:
	        if getSum > allLogProb[p]:
        	        big = getSum
                	small = allLogProb[p]
        	else:
                	big = allLogProb[p]
                	small = getSum
        	getSum =  big + math.log10(1 + math.pow(10, small - big))

	sum = getSum
	newProb = dict()
	for p in levels:
		newProb[p] = math.pow(10,allLogProb[p]-sum)
	
	sum2 = 0


	return newProb


cor = 0
incor = 0
for name in test:
    #print (name)
	with open(filefull + name) as f:
		for line in f:
			line = " " + line
		possibleDict = {}
		
	
		words = line.rstrip().split()
		#correctPres = words[0]
		#words = words[1:]
		possibleDict = guess(words)
		guessLevel = max(possibleDict, key=possibleDict.get)

		if correctLevel.get(name) == guessLevel:
			cor += 1
		else:
			incor += 1

print ("accuracy is ", cor, incor, cor/(cor+incor))	
