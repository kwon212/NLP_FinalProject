# NLP Final Project

Prof.Chiang's NLP Class Final Project:
Classify the Proficiency Level of a Written Text

Data folder contains all written texts and csv files from the ETS TOEFL corpus.
data parsing is done within src code.

Src folder contains all code:

guessFrequent.py

Guess the most frequently occuring level from the training data.

logisticregression.py

Use logistic regression to guess the proficiency level using a bag of words vocabulary.

linearregression.py: Uses Panda and sklearn linear regression toolkit

Use linear regression to combine all features to guess the proficiency level. This uses panda to generate the dataframe and the sklearn linear_model toolkit to fit the model (guess coefficients) and generate the correct Y value. The coefficient values need to be tweaked to reach the most optimal results. The coefficient and intercept values I used can be found within the code.

ckyParser.py

Generate the most probable POS parse and corresponding log probability.

baseline.py

Previous baseline file using word length/sentence length.

Need Python 3 to run the code.
