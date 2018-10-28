import nltk
import numpy as np
import os
import imutils
import pandas as pd

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

##########################################
##########################################

functionDict = {
  "remove_stops": lambda x,y: remove_stops(x,y),
  "compare_filtered_sentences": lambda x,y: compare_filtered_sentences(x,y),
  "remove_stops_file": lambda x: remove_stops_file(x),
}

##########################################
##########################################

stop_words_std = set(stopwords.words('english'))

#input a sentence (as string) and return sentence with stopwords removed
#as a list of strings, make choice of stopwords
def remove_stops(sentence, stopword_list):
    sentence = sentence.lower()
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [w for w in word_tokens if not w in stopword_list]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
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


def remove_stops_file(filepath):
    datafile = pd.read_csv(filepath)
    tweets_list = datafile['Tweet']
    filtered_tweets_list = []
    for tweet in tweets_list:
        filtered_tweet = remove_stops(tweet, stop_words_std)
        filtered_tweets_list.append(filtered_tweet)
    new_tweet_list_column_values = pd.Series(filtered_tweets_list)
    datafile.insert(loc=-1, column='filtered_tweet', value = new_tweet_list_column_values)
    pd.to_csv(filepath + 'filtered', datafile, index = 'FALSE')

##########################################
##########################################

def apply_function(filepath, function):
	if function in functionDict:
		temp = functionDict[function](filepath)
		return(temp)
	else:
		print "Sorry boss, I don't understand that command."

def run(filepath, function):
	apply_function(filepath, function)

##########################################
##########################################

def userinputloop():
	while True:
		prompt = raw_input("Apply to file? (y/n) ")

		if prompt == "y":
			filepath = raw_input("Please enter an file: ")
			function = raw_input("Please enter a function: ")
			run(filepath, function)
		elif prompt == "n":
			break
		else: print("Didn't catch that. Sorry.")

##########################################
##########################################

userinputloop()
