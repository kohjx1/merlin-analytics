#Importing required module
import numpy as np
from nltk.tokenize import  word_tokenize 

#Example text corpus for our tutorial
text = ['Topic sentences are similar to mini thesis statements.\
        Like a thesis statement, a topic sentence has a specific \
        main point. Whereas the thesis is the main point of the essay',\
        'the topic sentence is the main point of the paragraph.\
        Like the thesis statement, a topic sentence has a unifying function. \
        But a thesis statement or topic sentence alone doesn’t guarantee unity.', \
        'An essay is unified if all the paragraphs relate to the thesis,\
        whereas a paragraph is unified if all the sentences relate to the topic sentence.'
       ]
 
#Preprocessing the text data
sentences = []
word_set = []

for sent in text:
    x = [i.lower() for  i in word_tokenize(sent) if i.isalpha()]
    sentences.append(x)
    for word in x:
        if word not in word_set:
            word_set.append(word)

#Set of vocab 
word_set = set(word_set)
#Total documents in our corpus
total_documents = len(sentences)

#Creating an index for each word in our vocab.
index_dict = {} #Dictionary to store index for each word
i = 0
for word in word_set:
    index_dict[word] = i
    i += 1

#Create a count dictionary
 
def count_dict(sentences):
    word_count = {}
    for word in word_set:
        word_count[word] = 0
        for sent in sentences:
            if word in sent:
                word_count[word] += 1
    return word_count
 
word_count = count_dict(sentences)
print(word_count)

#Term Frequency
def termfreq(document, word):
    N = len(document)
    occurance = len([token for token in document if token == word])
    return occurance/N

#Inverse Document Frequency
def inverse_doc_freq(word):
    try:
        word_occurance = word_count[word] + 1
    except:
        word_occurance = 1
    return np.log(total_documents/word_occurance)

#TF-IDF
def tf_idf(sentence):
    tf_idf_vec = np.zeros((len(word_set),))
    for word in sentence:
        tf = termfreq(sentence,word)
        idf = inverse_doc_freq(word)
         
        value = tf*idf
        # index_dict[word] = value
        tf_idf_vec[index_dict[word]] = value 
    return tf_idf_vec
    # return index_dict

#TF-IDF Encoded text corpus
vectors = []
for sent in sentences:
    vec = tf_idf(sent)
    vectors.append(vec)
 
print(vec)