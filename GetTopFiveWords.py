import nltk
import numpy as np
import os
import pandas as pd
import datetime
import random
import itertools

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
def remove_stops(sentence):
    sentence = str(sentence)
    sentence = sentence.lower()
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stop_words_no_twitter_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words_no_twitter_words:
            filtered_sentence.append(w)
    return filtered_sentence


path = "/Users/alexbeckwith/Desktop/HACKOHIO/"
Extension = ""

TweetDF = pd.read_csv(path+Extension+"LakersSpursRounded.csv")
Counts = pd.read_csv(path + Extension + "LakersSpursBinCounts.csv")

TweetDF = TweetDF[['Time','Tweet']]
TweetDF = TweetDF.drop_duplicates()

Times = list(Counts.Time)

TopFive = []

i = 1
for time in Times:
    Words = map(remove_stops,TweetDF.loc[TweetDF.Time == time,'Tweet'].values)
    #Words = itertools.chain.from_iterable(Words)
    temp = []
    for item in Words:
        temp = temp + item
    Words = pd.DataFrame(temp,columns = ['Word'])


    TopFiveWords = list(Words['Word'].value_counts().index[0:10])
    TopFive.append(TopFiveWords)

Counts['TopFive'] = TopFive
Counts.to_csv(path+Extension+"TopFive.csv",index=False)
