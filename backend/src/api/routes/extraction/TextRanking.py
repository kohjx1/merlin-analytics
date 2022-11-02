import math
import re
from textblob import TextBlob as tb
from gensim.parsing.preprocessing import remove_stopwords

# filter based on operator/caller


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

# TF = (Number of time the word occurs in the text) / (Total number of words in text)
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

# Number of documents containing word
def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

# IDF = (Total number of documents / Number of documents with word t in it)
def idf(word, bloblist):
    return math.log(1 + len(bloblist) / (1 + n_containing(word, bloblist)))

# TF-IDF = TF * IDF
def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

# remove words based on custom stopwords
def removestopwords(sentence, stopwords):
    tokens = sentence.split(" ")
    tokens_filtered= [word for word in tokens if not word in stopwords]
    return (" ").join(tokens_filtered)

# get top keywords (sorting)
def generate_top_keywords(bloblist, filter):
  labels = []

  for i, blob in enumerate(bloblist):
      print("Top words in document {}".format(i + 1))
      scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
      sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
      for word, score in sorted_words[:filter]:
          labels.append({"group": word, "value": score})
          print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

  # sort JSON based on value (Top to Btm)
  labels.sort(key=lambda x: x["value"])

  return labels

# function (text ranking based on frequent words)
def freq_text_ranking(filter):
  # declare variables
  text = ""

  # convert array to string and lowercase all words
  for ts in transcript:
    text += " ".join(ts).lower()

  # remove tags
  text = re.sub("</?.*?>"," <> ",text)

  # remove special characters
  text = re.sub("(\\d|\\W)+"," ",text)

  # remove the stop words (unwanted words)
  # one from library, one from our custom stopwords (stopwords.txt)
  # e.g. "and", "you", "both", "from"
  stopwords_file = open("backend/resources/stopwords.txt", "r")
  lines = stopwords_file.read().splitlines()

  my_stopwords = lines
  
  document = remove_stopwords(text)
  document = removestopwords(text, my_stopwords)

  # TextBlob: Simplified Text Processing
  document = tb(document)

  bloblist = [document]
  
  # generate top keywords
  data = generate_top_keywords(bloblist, filter)
  return data
  
# function (text ranking based on operator)
def operator_text_ranking(filter):
  # declare variables
  text = ""
  sentence_array = []

  # convert array to string and lowercase all words
  for ts in transcript:
    for sentence in ts:
      if "o" in sentence.split()[0].lower():
        sentence_array.append(sentence.lower())

  text = "".join(sentence_array)

  # remove tags
  text = re.sub("</?.*?>"," <> ",text)

  # remove special characters
  text = re.sub("(\\d|\\W)+"," ",text)

  print(text)
  print()
  # remove the stop words (unwanted words)
  # one from library, one from our custom stopwords (stopwords.txt)
  # e.g. "and", "you", "both", "from"
  stopwords_file = open("backend/resources/stopwords.txt", "r")
  lines = stopwords_file.read().splitlines()

  my_stopwords = lines
  
  document = remove_stopwords(text)
  document = removestopwords(text, my_stopwords)

  # # TextBlob: Simplified Text Processing
  document = tb(document)

  bloblist = [document]

  # generate top keywords
  data = generate_top_keywords(bloblist, filter)
  print(data)
  return data

# function (text ranking based on operator)
def caller_text_ranking(filter):
  # declare variables
  text = ""
  sentence_array = []

  # convert array to string and lowercase all words
  for ts in transcript:
    for sentence in ts:
      if "c" in sentence.split()[0].lower():
        sentence_array.append(sentence.lower())

  text = "".join(sentence_array)

  # remove tags
  text = re.sub("</?.*?>"," <> ",text)

  # remove special characters
  text = re.sub("(\\d|\\W)+"," ",text)

  print(text)
  print()
  # remove the stop words (unwanted words)
  # one from library, one from our custom stopwords (stopwords.txt)
  # e.g. "and", "you", "both", "from"
  stopwords_file = open("backend/resources/stopwords.txt", "r")
  lines = stopwords_file.read().splitlines()

  my_stopwords = lines
  
  document = remove_stopwords(text)
  document = removestopwords(text, my_stopwords)

  # # TextBlob: Simplified Text Processing
  document = tb(document)

  bloblist = [document]

  # generate top keywords
  data = generate_top_keywords(bloblist, filter)
  print(data)
  return data


