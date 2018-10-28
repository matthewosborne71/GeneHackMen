#Routines for handling datetime type data from twitter

import datetime as dt
import math
import pandas as pd

def to_datetime(time_entry): #converts date+time string to datetime type
    format = '%Y-%m-%d %H:%M:%S'
    date = dt.datetime.strptime(time_entry, format)
    return(date)

def to_est(time): #converts from UTC time to EST time
    time = time - dt.timedelta(0,14400)
    return time

def round_down(time): #rounds datetime down to nearest minute
    time.replace(second = 0, microsecond = 0)
    return time

def rounded_est(timestring): #convert time string to preceding minute in EST
    time = pd.to_datetime(timestring)
    time.replace(hour = time.hour-4,second = 0, microsecond = 0)
    return time

#####above functions are for tailored rounding, below just round down to minute


def nosec(timestring): #removes the 'second' part of date-time string
    return timestring[:-2] + '00'

def append_timebins(filepath): #adds column for binned times to Tweet dataframe
    df = pd.read_csv(filepath)
    #times = rawTW['Created_At']
    times = df['Created_At']
    rounded = [nosec(time) for time in times]
    df['Timebin'] = rounded
    return df

def timebin_counts(filepath): #returns dataframe indexed by timestring with number of tweets at each time
    df = append_timebins(filepath)
    return df['Timebin'].value_counts().sort_index()




raw = pd.read_csv('Data/PittsburghPull_Tweets.csv')
times = raw['Created_At']
