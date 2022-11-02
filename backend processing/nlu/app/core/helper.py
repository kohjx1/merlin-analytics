from typing import List, Tuple
import nltk
import os

nltk.data.path.append(os.path.join(os.getcwd(), "resources", "nltk_data"))
STOP_WORDS = set(nltk.corpus.stopwords.words('english'))


def pre_process_text(text: str, stop: bool = False, lemma: bool = False, stem: bool = False) -> List[str]:
    """
    Perform pre-processing on string:
    1. Convert to lower case
    2. Tokenization
    3. Remove stop words (optional)
    4. Lemmatization (optional)
    5. Stemming (optional)
    """  
    # 1. convert lower case
    text = text.lower()

    # 2. tokenization
    sentences = nltk.tokenize.sent_tokenize(text)   # split by sentences
    text_tokens = []
    for s in sentences:
        tokens = nltk.tokenize.word_tokenize(s)     # split by words      
        # 3. Remove stop words
        if stop:
            tokens = [w for w in tokens if not w in STOP_WORDS]
        text_tokens += tokens

    # 4. lemmatization using wordnet model
    if lemma:
        lemmatizer = nltk.stem.WordNetLemmatizer()
        text_tokens = [lemmatizer.lemmatize(w) for w in text_tokens]

    # 5. stemming using snowball model
    if stem:
        stemmer = nltk.stem.SnowballStemmer("english")
        text_tokens = [stemmer.stem(w) for w in text_tokens]

    return text_tokens


def is_subsequence(keywords: List[str], words: List[str]) -> bool:
    """
    Checks if keywords list is a strict subsequence of words list. Useful in cases
    where the keyword entry contains multiple words.
    """
    matched = False
    j = 0
    for i in range(len(keywords)):
        while j < len(words):
            if keywords[i] == words[j]:
                matched = True 
                j += 1
                break 
            elif matched:
                return False
            j += 1
    
    return matched


NUMBER_DICT = {
    "zero": {"value": 0, "scale": 1},
    "one": {"value": 1, "scale": 1},
    "two": {"value": 2, "scale": 1},
    "three": {"value": 3, "scale": 1},
    "four": {"value": 4, "scale": 1},
    "five": {"value": 5, "scale": 1},
    "six": {"value": 6, "scale": 1},
    "seven": {"value": 7, "scale": 1},
    "eight": {"value": 8, "scale": 1},
    "nine": {"value": 9, "scale": 1},
    "ten": {"value": 10, "scale": 10},
    "eleven": {"value": 11, "scale": 10},
    "twelve": {"value": 12, "scale": 10},
    "thirteen": {"value": 13, "scale": 10},
    "fourteen": {"value": 14, "scale": 10},
    "fifteen": {"value": 15, "scale": 10},
    "sixteen": {"value": 16, "scale": 10},
    "seventeen": {"value": 17, "scale": 10},
    "eighteen": {"value": 18, "scale": 10},
    "nineteen": {"value": 19, "scale": 10},
    "twenty": {"value": 20, "scale": 10},
    "thirty": {"value": 30, "scale": 10},
    "forty": {"value": 40, "scale": 10},
    "fifty": {"value": 50, "scale": 10},
    "sixty": {"value": 60, "scale": 10},
    "seventy": {"value": 70, "scale": 10},
    "eighty": {"value": 80, "scale": 10},
    "ninety": {"value": 90, "scale": 10},
    "hundred": {"value": 100, "scale": 100},
    "thousand": {"value": 1000, "scale": 1000}, 
    "million": {"value": 1000000, "scale": 1000000}, 
    "billion": {"value": 1000000000, "scale": 1000000000}, 
    "trillion": {"value": 1000000000000, "scale": 1000000000000}
}


def get_numeric_answer(text: str) -> Tuple[str, List[str]]:
    """
    Look for numeric words in input text and convert it to integer. 
    NOTE: This assumes that the ASR produces numbers as words, not digits
    """
    text_tokens = pre_process_text(text)
    
    numbers = []
    for token in text_tokens:
        if token == "and" or token == ",":
            continue
        if token in NUMBER_DICT.keys():
            numbers.append(token)
        elif numbers:
            break
        
    if not numbers:
        return None, []
    return str(text2int(numbers)), [" ".join(numbers)]


def text2int(numbers: List[str]) -> int:
    """
    Combines a list of numeric words into a single integer value. 
    """
    # look for largest scale in the list and splits the list at that point
    max_index = 0
    max_scale = 1
    for i in range(len(numbers)):
        if NUMBER_DICT[numbers[i]]["scale"] > max_scale:
            max_index = i
            max_scale = NUMBER_DICT[numbers[i]]["scale"]
    
    # if max_scale is less than 100, just concatenate numbers in the list
    # example of max_scale < 100 -> 76, 85, 23, etc
    # example of max_scale >= 100 -> 205, 1430, etc
    if max_scale < 100:
        curr_val, curr_scale = NUMBER_DICT[numbers[0]]["value"], NUMBER_DICT[numbers[0]]["scale"]
        for i in range(len(numbers) - 1):
            next_val, next_scale = NUMBER_DICT[numbers[i+1]]["value"], NUMBER_DICT[numbers[i+1]]["scale"]
            if next_scale < curr_scale:     # eg. seventy six
                curr_val += next_val
            else:                           # eg. nineteen twenty
                curr_val = curr_val * next_scale * 10 + next_val
        return curr_val

    # makes use of recursion to sum the values if max_scale is more than 100
    if max_index == len(numbers) - 1:
        return text2int(numbers[:max_index]) * max_scale    # in cases where the max_scale is at the end of the list (eg. three thousand)
    else:
        return text2int(numbers[:max_index]) * max_scale + text2int(numbers[max_index+1:])
