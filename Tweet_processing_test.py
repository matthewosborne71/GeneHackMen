import nltk
import numpy as np
import os
import imutils
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

punctuation = set([u'.', u',', u';', u':', u'!', u'?', u'&'])
other_grammar = set([u'us', u'we', u'my', u'his', u'could', u'would', u'should',
u'might', u'may', u'can', u'maybe'])
stop_words_std = set(stopwords.words('english')).union(punctuation).union(other_grammar)


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

#input two filtered sentences (as list of strings) and return the words they have
#in common as a list of strings
def compare_filtered_sentences(f_sentence1, f_sentence2):
    common_words = []
    for w in f_sentence1:
        if w in f_sentence2:
            common_words.append(w)
    return(common_words)

#input a filepath to a csv file with sentence data. Remove stopwords from
#each sentence, and save new file with filtered sentences (as lists of strings).
def remove_stops_file(filepath):
    datafile = pd.read_csv(filepath)
    new_column_number = len(datafile.columns)
    tweets_list = datafile['Tweet']
    filtered_tweets_list = []
    for tweet in tweets_list:
        filtered_tweet = remove_stops(tweet, stop_words_std)
        filtered_tweets_list.append(filtered_tweet)
    new_tweet_list_column_values = pd.Series(filtered_tweets_list)
    datafile.insert(loc=new_column_number, column='filtered_tweet', value = new_tweet_list_column_values)
    newfilename = filepath.replace('.csv','')
    datafile.to_csv(newfilename + "filtered.csv", index = False)

remove_stops_file("Data/PittsburghPull_Tweets.csv")
