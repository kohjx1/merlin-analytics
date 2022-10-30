# declare imports
import re
import math
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# TF = No. of repetition of words in a sentence / Total words in a sentence
# IDF = log(No. of sentence / No. of sentences containing word)
# TDIDF = TF * IDF

# read the fire keywords json file (keywords_fire.txt)
with open('backend/resources/keywords_fire.json', encoding='utf-8') as file:
    data = json.load(file)

bowFire = []
for i in data:
  for key, value in i.items():
    for items in value:
      bowFire.append(items)

print("Keywords - Fire")
print("====================================")
print(bowFire)
print()

# read the medical keywords json file (keywords_med.txt)
with open('backend/resources/keywords_med.json', encoding='utf-8') as file:
    data = json.load(file)

bowMedical = []
for i in data:
  for key, value in i.items():
    for items in value:
      bowMedical.append(items)

print("Keywords - Medical")
print("====================================")
print(bowMedical)
print()

# sample of compiled transcripts (array of arrays)
# data will be taken from database
transcript = [
                [
                  "O; Hello this is 995 how may i help you?",
                  "C; Hi i need an ambulance now, got one auntie here she's injured.",
                  "O; okay can you give me the address?",
                  "C; err okay we are below this condo Katong Park Towers, i think the postal code is 439826.",
                  "O; okay let me check. Is it at 114A Arthur Road?",
                  "C; ya i think so",
                  "O; okay what happened there?",
                  "C; No, I don't think so.",
                  "C; Just now got one robber, he snatched the auntie's handbag then pushed her! She fell down on the ground and injured her hands and legs. And I think she knocked her head on the ground.",
                  "O; okay the lady roughly how old?",
                  "C; She's around 60 years old.",
                  "O; sixty years old, is she conscious at the moment?",
                  "C; She's conscious but she seems a bit drowsy.",
                  "O; okay please hold on i'm rushing out the ambulance for you. Does she have any breathing difficulty?",
                  "C; Hmm she seems to be panting a little.",
                  "O; okay my ambulance is on the way already how may i address you.",
                  "C; Henry",
                  "O; okay Henry, so you just keep her in a comfortable position, monitor her if her condition gets worse you can call us back at nine nine five.",
                  "C; okay so the the the ambulance coming now right?",
                  "O; yes on the way already so your address is 114A Arthur Road right?",
                  "C; yes okay thanks ",
                  "O; okay thank you bye"
                ],
                [
                  "O;	hello this is nine nine five how can i help you hi.",
                  "C;	eh hi yah i need ambulance now.",
                  "O;	okay please hold on. can you give me the address.",
                  "C;	okay the postal code is two four eight three six four.",
                  "O;	two four eight three three six four.",
                  "C;	yah.",
                  "O;	okay please hold on let me check it's at four seven nine river-valley-road.",
                  "C;	yah the unit number.",
                  "O;	okay unit number.",
                  "C;	my father fell and.",
                  "O;	your father roughly how old.",
                  "C;	my father is eighty three.",
                  "O;	eighty three is he conscious at the moment."
                  "C;	he's conscious but he's not answering my question.",
                  "O;	okay please hold on i'm rushing out the ambulance for you.",
                  "C;	no i have oxygen at home so i'm giving him oxygen oxygen level is ninety three.",
                  "O;	okay and is he drowsy or alert now.",
                  "C;	drowsy very drowsy.",
                  "O;	drowsy okay my ambulance is on the way already how may i address you.",
                  "C;	john",
                  "O;	okay john so you just keep him in a comfortable position monitor him if his condition gets worse you can call us back at nine nine five.",
                  "C;	okay so the the the ambulance coming now right.",
                  "O;	yes on the way already so your address is four seven nine river-valley-road.",
                  "C;	yes correct okay thank you yes thanks bye bye.",
                  "O;	okay thank you john bye."
                ],
                [
                  "O;	hello this is nine nine five how may i help you.",
                  "C;	hi yah i need an ambulance now err there's someone lying down there unconscious.",
                  "O;	okay can you give me the address.",
                  "C;	not very sure i'm in punggol below this err h d b. two seven zero b.",
                  "O;	okay let me check. is it at two seven zero b punggol field.",
                  "C;	ya i think so.",
                  "O;	okay what happened there.",
                  "C;	err this encik he's lying down there i think he's unconscious i called out to him but he's not responding and hor got a pungent smell in the air it's like 猫 山 王 榴 莲 like that.",
                  "O;	okay unconscious is he breathing.",
                  "C;	i think he's breathing seems quite heavy. looks quite jialat.",
                  "O;	okay how old is he.",
                  "C;	err i think he's around fifty years old.",
                  "O;	okay please hold on i'm rushing out the ambulance for you now how may i address you."
                  "C;	john.",
                  "O;	okay john help is on the way already."
                ],
                [
                  "O; Nine nine five, what's your emergency?",
                  "C; Someone just fainted.",
                  "O; Okay, what is the address of the emergency?",
                  "C; I'm outside Ikea. The one at Alexandra.",
                  "O; Okay, is the addres 317 Alexandra Rd?",
                  "C; Yes I think so.",
                  "O; Okay, I have dispatched an ambulance to your location.",
                  "C; Thanks.",
                  "O; Can you check if the person is breathing?",
                  "C; Hold on let me check. Yeah, I think so.",
                  "O; Okay, that's great. How may I addres you?",
                  "C; Susan;",
                  "O; Okay Susan, can you get the person into recovery position?",
                  "C; Okay I think so.",
                  "O; Okay that's great, the ambulance is on its way. Thank you Susan, bye."
                ],
                [
                  "O; 995, what's your emergency?",
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
                ],
             ]

# declare variables
text = ""
wordsFiltered = []
wordList = []
labels = []

# convert array to string and lowercase all words
for ts in transcript:
  text += " ".join(ts).lower()

# remove tags
text = re.sub("</?.*?>"," <> ",text)

# remove special characters
text = re.sub("(\\d|\\W)+"," ",text)

# convert string back to array
text = text.split(" ")

# remove blank field
for txt in text:
  if txt == "":
    text.remove(txt)

print("Transcript - Text")
print("====================================")
print(text)
print()

# read custom stopwords.txt
stopwords_file = open("backend/resources/stopwords.txt", "r")
lines = stopwords_file.read().splitlines()

stopWords = set(stopwords.words('english') + lines)

# remove the stop words (unwanted words)
# e.g. "and", "you", "both", "from"
for word in text:
    if word not in stopWords and word != "":
        wordsFiltered.append(word)

# automatically remove any duplicate words
unrepeatedWords = set(wordsFiltered)

print("Transcript - Filtered Text [removed unwanted words]")
print("====================================")
print(unrepeatedWords)
print()

# create a dictionary of unique words
numOfWords = dict.fromkeys(unrepeatedWords, 0)

# NOTE: try not to hardcode (there could be more than these two keywords array)
# store fire keywords
for word in bowFire:
  wordList.append(word)

# store medical keywords
for word in bowMedical:
  wordList.append(word)

# remove duplicates in wordlist
wordList = list(dict.fromkeys(wordList))

print("Word Dictionary - Unique Word [before count]")
print("====================================")
print(numOfWords)
print()


for index, txt in enumerate(text):
  print(index)
  print(txt)
  if txt in wordList:
    print("[keyword]")
    numOfWords[txt] += 1

print("Word Dictionary - Unique Word [after count]")
print("====================================")
print(numOfWords)
print()

def computeTF(wordDict, bow):
  tfDict = {}
  bowCount = len(bow)
  for word, count in wordDict.items():
    tfDict[word] = count/float(bowCount)
  return tfDict

tfBow = computeTF(numOfWords, wordList)

print("TF Bow")
print("====================================")
print(tfBow)

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
    if (val == 0):
      idfDict[word] = float(0)
    else:
      idfDict[word] = math.log((N+1)/float(val)+1.0)
  
  return idfDict

idfs = computeIDF([numOfWords])
print("IDF")
print("====================================")
print(idfs)
print()
  
def computeTFIDF(tfBow, idfs):
  tfidf = {}

  for word, val in tfBow.items():
    tfidf[word] = val*idfs[word]
  return tfidf

tfidfBow = computeTFIDF(tfBow, idfs)

print("TFIDF")
print("====================================")
print(pd.DataFrame([tfidfBow]))
print()

# serializing JSON
for key, val in tfidfBow.items():
  if val > 0 and key in bowFire and key in bowMedical:
    labels.append({"word": key, "value": val, "group": "Fire & Medical"})
  elif val > 0 and key in bowFire:
    labels.append({"word": key, "value": val, "group": "Fire"})
  elif val > 0 and key in bowMedical:
    labels.append({"word": key, "value": val, "group": "Medical"})

# sort JSON based on value (Top to Btm)
labels.sort(key=lambda x: x["value"], reverse=True)

# writing to wordcloudData.json 
with open("frontend/src/lib/data/wordcloudData.json", "w+") as f:
    json.dump(labels, f, indent=4)

print("wordcloudData.json is created")
print()

# from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf = TfidfVectorizer()
# response = tfidf.fit_transform(text)

# print(pd.DataFrame(response.toarray(), columns = tfidf.get_feature_names_out()))