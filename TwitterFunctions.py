## TwitterFunctions ##
## !0 27 2018
## Matthew Osborne


## This code was written for the HackOHI/O 2018 competition for the
## GeneHackMen Team

## It was used to search queried tweets

# Import the packages we need
from tweepy import Cursor
import datetime
import time
import unicodedata
import logging

# clean strings before writing to file
def CleanThatString(string):
    output = unicodedata.normalize('NFKD',string).encode('ascii','ignore')
    output = str(output)
    output = str.replace(output, '\n', '')
    output = str.replace(output, '\r', '')
    output = str.replace(output, ',', '')
    output = str.replace(output,"'",'')
    output = str.replace(output,'"','')
    return output[0:]

# Get the specific client we want to pull the data
def GetClient(NumClients,clients,i):
    if NumClients == 2:
        if i%NumClients == 0:
            return clients[0]
        else:
            return clients[1]
    else:
        if i%NumClients == 0:
            return clients[0]
        elif i%NumClients == 1:
            return clients[1]
        else:
            return clients[2]

# This function will search Twitter for specific functions
def SearchTwitter(clients,since_id,path,Queries,FileName,Stopper):
    # How many clients are we using?
    NumClients = len(clients)
    First = True

    # Open all of the files that we will be writing to
    tweets = open(path + FileName + "_Tweets.csv","w+")
    tweets.write("User,UserID,Query,TweetID,Created_At,Retweet_Count,Favorite_Count,IsRT,Tweet\n")
    retweets = open(path + FileName + "_Retweets.csv","w+")
    retweets.write("User,UserID,Query,ResultID,ResultCreated_At,RTUser,RTID,RT_created_at,RT_text\n")
    hts = open(path + FileName + "_Hashtags.csv","w+")
    hts.write("User,UserID,query,TweetID,created_at,hashtag\n")
    ments = open(path + FileName + "_Ments.csv","w+")
    ments.write("User,UserID,Query,TweetID,Created_At,Mention\n")
    links = open(path + FileName + "_Links.csv","w+")
    links.write("User,UserID,Query,TweetID,Created_At,URL\n")



    # This loop pulls the data
    i = 0
    while i < Stopper:
        logging.info("Going through the loop for the " + str(i) + "th time.\n")
        i = i+1
        client = GetClient(NumClients,clients,i)

        # Determine how many seconds to sleep through pulls
        if NumClients == 2:
            sleep = 30
        else:
            sleep = 20

        if First != True:
            since_id = result_id
        else:
            First = False

        # Randomly choose a query from our query list, then find the 1500 most recent tweets about that query
        query = Queries.sample()['query'].values[0]
        logging.info("Getting results for " + str(query) + " query.\n")
        Search = Cursor(client.search, q = query,count = 100,result_type="recent",include_entities=True,tweet_mode='extended').pages(10)

        # Write the data to file
        for page in Search:
            for result in page:
                if 'retweeted_status' in dir(result):
                    retweet = True
                    RTUser = result.retweeted_status.user.screen_name
                    tweet = result.retweeted_status.full_text
                    RT_ID = result.retweeted_status.id_str
                    RT_created_at = str(result.retweeted_status.created_at)
                else:
                    retweet = False
                    tweet = result.full_text

                screen_name = result.user.screen_name
                user_id = result.user.id_str
                result_id = result.id_str
                created_at = str(result.created_at)
                retweet_count = str(result.retweet_count)
                favorite_count = str(result.favorite_count)
                tweet = CleanThatString(tweet)

                if retweet:
                    RTtext = tweet
                    tweet = "RT @" + RTUser + ": " + RTtext
                    retweets.write(screen_name + "," + user_id + "," + query + ","
                                    + result_id + "," + created_at + "," + RTUser +"," + RT_ID +
                                    "," + RT_created_at + "," + CleanThatString(result.retweeted_status.full_text) + "\n")

                tweets.write(screen_name + "," + user_id + "," + query + "," + result_id + ","
                            + created_at + "," + retweet_count + "," + favorite_count +"," + str(retweet)
                            + "," + tweet +"\n")

                for hashtag in result.entities['hashtags']:
                    hts.write(screen_name + "," + user_id + "," + query + "," + result_id
                                + "," + created_at + "," + CleanThatString(hashtag['text']) + "\n")
                for mention in result.entities['user_mentions']:
                    ments.write(screen_name + "," + user_id + "," + query + "," + result_id
                                + "," + created_at + "," + str(mention['screen_name']) + "\n")
                for url in result.entities['urls']:
                    links.write(screen_name + "," + user_id + "," + query + "," + result_id
                                + "," + created_at + "," + str(url['expanded_url']) + "\n")

        logging.info("Sleeping for " + str(sleep) + " seconds before next pull.\n")
        time.sleep(sleep)


    tweets.close()
    retweets.close()
    hts.close()
    ments.close()
    links.close()
    logging.info("Now exiting the data pull.\n")
