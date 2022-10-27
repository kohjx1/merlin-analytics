# TF = No. of repetition of words in a sentence / Total words in a sentence
# IDF = log(No. of sentence / No. of sentences containing word)
# TDIDF = TF * IDF

# declare imports
import re
import math
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# Keywords (fire)
bowFire = [
    "fire",
    "smoke",
    "engine",
    "black smoke",
    "white smoke",
    "white flames",
    "explosion",
    "explode",
    "gas",
    "electric bike",
    "electric scooter",
    "gas cylinder",
    "lpg",
    "molotov",
    "oil drum",
    "pallets",
]

# Keywords (medical)
bowMedical = [
    "ambulance",
    "polyclinic",
    "faint",
    "pain",
    "sick",
    "fall",
    "fell",
    "drowsy",
    "breathing",
    "conscious",
    "bleeding",
    "bleed",
    "blood",
]

# Sample Transcript
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

# declare variables
wordsFiltered = []

# read custom stopwords.txt
stopwords_file = open("backend/resources/stopwords.txt", "r")
lines = stopwords_file.read().splitlines()

stopWords = set(stopwords.words('english') + lines)
print("StopWords")
print("------------")
print(stopWords)
print()

# remove the stop words (unwanted words)
# e.g. "and", "you", "both", "from"
for w in text:
    if w not in stopWords and w != "":
        wordsFiltered.append(w)

# automatically remove any duplicate words
unrepeatedWords = set(wordsFiltered)

# create a dictionary of unique words
numOfWords = dict.fromkeys(unrepeatedWords, 0)

wordList = [bowFire, bowMedical]

print("Word Dictionary - Initial")
print("---------------------------")
print(numOfWords)
print()

# for t in text:
#   for words in wordList:
#     for word in words:
#       if word in t:
#         print(word)
#         numOfWords[word] += 1

for word in wordsFiltered:
    numOfWords[word] += 1

print("Word Dictionary - Count")
print("-------------------------")
print(numOfWords)
print()

def computeTF(wordDict, bow):
  tfDict = {}
  bowCount = len(bow)
  for word, count in wordDict.items():
    tfDict[word] = count/float(bowCount)
  return tfDict

tfBow = computeTF(numOfWords, wordsFiltered)

print("TF Bow")
print("------------------")
print(tfBow)
print()

def computeIDF(docList):
  idfDict = {}
  N = len(docList)

  # {"key":value}
  idfDict = dict.fromkeys(docList[0].keys(), 0)

  # find num of docs which contains word
  for doc in docList:
    for word, val in doc.items():
      if val > 0:
        idfDict[word] += 1
  
  for word, val in idfDict.items():
      idfDict[word] = math.log(N/float(val))
  
  return idfDict

idfs = computeIDF([numOfWords])
print("IDF")
print("------------------")
print(idfs)
print()
  
def computeTFIDF(tfBow, idfs):
  tfidf = {}

  for word, val in tfBow.items():
    tfidf[word] = val*idfs[word]
  return tfidf

tfidfBow = computeTFIDF(tfBow, idfs)

print("TFIDF")
print("------------------")
print(pd.DataFrame([tfidfBow]))

# serializing JSON
# labels = []

# for key, val in tfidfBow.items():
#   if val > 0:
#     labels.append({"word": key, "value": val, "group": "First"})

# # writing to sample.json
# with open("frontend/src/lib/data/sample.json", "w+") as f:
#     json.dump(labels, f, indent=4)

    
# from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf = TfidfVectorizer()
# response = tfidf.fit_transform(text)

# print(pd.DataFrame(response.toarray(), columns = tfidf.get_feature_names_out()))


# TFIDF - Term Ranking
# 2 Documents (Fire, Medical)
# Charts can be filtered by Fire/Medical
# WordCloud (2 groups based on documents)
# BarChart (other keywords - percentage)
# DonutChart (gender/age?)