import nltk
import numpy as np
import os
import imutils
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

#input two filtered sentences (as list of strings) and return the words they have
#in common as a list of strings
def compare_filtered_sentences(f_sentence1, f_sentence2):
    common_words = []
    for w in f_sentence1:
        if w in f_sentence2:
            common_words.append(w)
    return(common_words)

'''def compare_filtered_sentences_file(filepath):
    datafile = pd.read_csv(filepath)
    new_column_number = len(datafile.columns)
    tweets_list = datafile['filtered_tweet']
    for tweet1 in tweets_list:
        for tweet2 in tweets_list:
            temp_common_words = compare_filtered_sentences(tweet1, tweet2)'''

def most_common_words(filepath):
    wordlist = []
    datafile = pd.read_csv(filepath)
    new_column_number = len(datafile.columns)
    tweets_list = datafile['filtered_tweet']
    for tweet in tweets_list:
        for w in tweet:
            wordlist.append(w)
    tempwordcountlist = []
    i=0
    for w1 in wordlist:
        if wordlist.count(w1) > 50:
            if wordlist.index(w1) == i:
                count_w1 = 0
                for w2 in wordlist:
                    if w1 == w2:
                        count_w1 = count_w1 + 1
                tempwordcountlist.append((w1,count_w1))
            i = i+1
    tempwordcountlist.sort(key=itemgetter(1))
    finalwordlist = []


def RT_sampling(filepath):



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
    return(datafile)
    newfilename = filepath.replace('.csv','')
    datafile.to_csv(newfilename + "_filtered.csv", index = False)

#input time in UTC (eg "2018-10-27 17:56:41") as a string and convert to datetime
#object and return
def time_to_datetime(time_entry):
    format = '%Y-%m-%d %H:%M:%S'
    date = datetime.datetime.strptime(time_entry, format)
    return(date)

#input a filepath to a csv file with UTC times saved as strings. Convert each of
#these to datetime and returns the dataframe with the datetime.
def time_to_datetime_file(filepath):
    datafile = pd.read_csv(filepath)
    cols = datafile.columns.tolist()
    index = cols.index('Created_At')
    UTCtimes_list = datafile['Created_At']
    datetimes_list = []
    for time in UTCtimes_list:
        datetime_temp = time_to_datetime(time)
        datetimes_list.append(datetime_temp)
    new_datetime_list_column_values = pd.Series(datetimes_list)
    del datafile['Created_At']
    datafile.insert(loc=index, column='Created_At', value = new_datetime_list_column_values)
    return(datafile)


most_common_words("Data/PittsburghPull_Tweets.csv")


#savefileas input
#return list of top 5 words for Jason
