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

#input a filepath to a csv file with sentence data. Input file should be retweets
#file to make the later computations faster. Removes stopwords from
#each sentence, and returns new dataframe with filtered sentences (as lists of strings).
def remove_stops_file(filepath):
    datafile = pd.read_csv(filepath)
    new_column_number = len(datafile.columns)
    tweets_list = datafile['RT_text']
    filtered_tweets_list = []
    for tweet in tweets_list:
        filtered_tweet = remove_stops(tweet, stop_words_no_twitter_words)
        filtered_tweets_list.append(filtered_tweet)
    new_tweet_list_column_values = pd.Series(filtered_tweets_list)
    datafile.insert(loc=new_column_number, column='filtered_tweet', value = new_tweet_list_column_values)
    datafile.to_csv("filtered.csv", index = False)
    print("Removed stops")
    return(datafile)

def adj_matrix(dffiltered):
    wordlist = []
    thresh = raw_input("Input threshhold: ")
    threshhold = int(float(thresh))
    fil_tweet_list = dffiltered['filtered_tweet']
    cols = dffiltered.columns.tolist()
    index = cols.index('filtered_tweet')
    print(index)
    for tweet in fil_tweet_list:
        for w in tweet:
            wordlist.append(w)
    countlistnum = []
    countlistword = []
    print(len(wordlist))
    wordset = set(wordlist)
    listwordset = list(wordset)
    print(len(listwordset))
    for w in listwordset:
        tempcount = wordlist.count(w)
        if tempcount>threshhold:
            countlistnum.append(tempcount)
            countlistword.append(w)
    ftl = []
    for tweet in fil_tweet_list:
        ftl.append(tweet)
    print(type(ftl))
    print(len(ftl))
    for tweet in ftl:
        temp = tweet
        j = ftl.index(tweet)
        for w in tweet:
            if w not in countlistword:
                temp.remove(w)
        ftl[j] = temp
    del dffiltered['filtered_tweet']
    dffiltered.insert(loc=index, column='key_words', value = ftl)
    randomlist = random.sample(ftl,2000) #2000 random tweets chosen, might need fewer though
    M = []
    for w1 in countlistword:
        templist = []
        for w2 in countlistword:
            count = 0
            for tweet in randomlist:
                if w1 in tweet:
                    if w2 in tweet:
                        count = count + 1
            templist.append(count)
        M.append(templist)
    MaxList = []
    for e in M:
        temp = max(e)
        MaxList.append(temp)
    NormM = []
    for e in MaxList:
        i = MaxList.index(e)
        temp2 = M[i]
        new = [float(x)/float(e) for x in temp2]
        NormM.append(new)
    AdMat2 = pd.DataFrame(data = {'rows':NormM,'words':countlistword,'index_count':MaxList})
    AdMat2.to_csv("AdjacencyMatrix.cvs",index = False)
    return(dffiltered)


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


df = remove_stops_file("Data/PittsburghPull_Retweets.csv")
adj_matrix(df)
