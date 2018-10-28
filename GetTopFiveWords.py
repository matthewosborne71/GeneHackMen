import nltk
import numpy as np
import os
import pandas as pd
import datetime
import random

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from operator import itemgetter


#############################################
#STOP WORD LISTS
#############################################
punctuation = set([u'.', u',', u';', u':', u'!', u'?', u'&', u'-', u'(', u')'])
other_grammar = set([u'us', u'we', u'my', u'his', u'could', u'would', u'should',
u'might', u'may', u'can', u'maybe', u'http', u'https', u'url'])
twitter_words = set([u'@', u'http', u'https', u'url', u'rt', u'--', u'-', u'#'])

stop_words_std = set(stopwords.words('english')).union(punctuation).union(other_grammar)
stop_words_no_twitter_words = set(stop_words_std).union(twitter_words)

#############################################
#FUNCTIONS
#############################################

#input a sentence (as string) and return sentence with stopwords removed
#as a list of strings, make choice of stopwords
def remove_stops(sentence, stopword_list):
    sentence = sentence.lower()
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stopword_list]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stopword_list:
            filtered_sentence.append(w)
    return(filtered_sentence)


path = r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\GeneHackMen\\Data\\"
Extension = r"PittsburghData\\"

TweetDF = pd.read_csv(path+Extension+"PittsburghRounded.csv")
Counts = pd.read_csv(path + Extension + "PittsburghBinCounts.csv")

TweetDF = TweetDF[['Time','Tweet']]
TweetDF = TweetDF.drop_duplicates()

Times = list(Counts.Times)

Counts['TopFive'] = 0

for time in Times:
    Words = map(remove_stops,TweetDF.loc[TweetDF.Time == time,'Tweet'].values())

    TopFiveWords = list(Words.value_counts.index[0:5])

Counts.to_csv(path+Extension+"Test.csv",index=False)
