#Routines for hashtag processing from a body of tweets

import nltk as nl
import pandas as pd
import math


def HT_frequencies(HTfilepath): #given filepath to csv with hashtags organized by tweet, returns freq dist
    HT_raw = pd.read_csv(HTfilepath)
    frequencies = HT_raw['hashtag'].value_counts()
    hashtags = frequencies.index.values
    HT_freq_dist = pd.DataFrame({'hashtag':frequencies.index.values,'frequency':list(frequencies)},
    columns = ['hashtag','frequency'])
    return HT_freq_dist


def top_HT(freq_dist, pct): #given a freq_dist dataframe, returns the top pct entries
    num_top_entries = math.ceil(pct*len(freq_dist))
    return freq_dist.head(num_top_entries)

def HT_adjacency(topHTlist,HTfilepath): #given raw hashtag file organized by tweet
#and a list of top hashtags, returns an adjacency matrix
#(how frequently does each pair of top hashtags appear in the same tweet?)
    rawHT = pd.read_csv('HTfilepath')
    topHTlist2 = topHTlist
    HTpairs = [] #initialize adjacency matrix
    for x in topHTlist:
        topHTlist2.remove(x)
        for y in topHTlist2:
            HTpairs.append((x,y))
    HTadj = {}
    for pair in HTpairs:
        HTadj[pair] = 0
    for ht in topHTlist:
        httweets = rawHT.loc[rawHT.hashtag == ht, ['TweetID','hashtag']]
        for tid in httweets:
    
