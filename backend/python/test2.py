# declare imports
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# sample transcript
transcript = ["O; 995, what's your emergency?",
              "C; Hi, I think there is a fire at my neighbour's place. There is a lot of smoke coming from the window.",
              "O; Okay, can I get your address?",
              "C; The ppstal code is 530909.",
              "O; So it's 909 Hougang Street 91?",
              "C; Yes that's right.",
              "O; Is anyone injured? Do you need an ambulance?",
              "C; No, I don't think so.",
              "O; Okay, a fire truck is on its way. How may I address you?",
              "C; Jack.",
              "O; Okay Jack, evacuate the building as soon as possible. ",
              "C; Okay.",
              "O; Okay, thank you Jack. Goodbye."
             ]

# convert array to string and lowercase all words
text = " ".join(transcript).lower()

# remove tags
text = re.sub("</?.*?>"," <> ",text)

# remove special characters
text = re.sub("(\\d|\\W)+"," ",text)

# convert string back to array
text = text.split(" ")

# remove single characters
# new_text = ""
# for w in text:
#     if len(w) > 1:
#       new_text = new_text + " " + w

# declare variables
wordsFiltered = []
stopWords = set(stopwords.words('english'))

# remove the stop words (unwanted words)
# e.g. "and", "you", "both", "from"
for w in text:
    if w not in stopWords and w != "":
        wordsFiltered.append(w)

# automatically remove any duplicate words
unrepeatedWords = set(wordsFiltered)

# create a dictionary of unique words
numOfWords = dict.fromkeys(unrepeatedWords, 0)

# get occurence for each document in the corpus (collection of documents)
for word in wordsFiltered:
  numOfWords[word] += 1

print(numOfWords)
print()

# TF = No. of repetition of words in a sentence / Total words in a sentence
def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

tfBow = computeTF(numOfWords, wordsFiltered)
print(tfBow)

# IDF = log(No. of sentence / No. of sentences containing word)
def computeIDF(documents):
    import math
    N = len(documents)
    
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

idfs = computeIDF(numOfWords)

print(idfs)