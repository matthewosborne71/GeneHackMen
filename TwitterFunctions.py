import GetAPICred as Cred
from tweepy import Cursor
import datetime
import time
import unicodedata

def CleanThatString(string):
    output = unicodedata.normalize('NFKD',string).encode('ascii','ignore')
    output = str(output)
    output = str.replace(output, '\n', '')
    output = str.replace(output, '\r', '')
    output = str.replace(output, ',', '')
    output = str.replace(output,"'",'')
    output = str.replace(output,'"','')
    return output[0:]

clients = Cred.get_twitter_client()

def SearchTwitter(path,Queries,FileName):
    #Note Queries should be limited to 4 queries
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

    client = clients[0]
    i = 0
    while i < 10:
        i = i+1
        print i
        for query in Queries:
            print query
            Search = Cursor(client.search, q = query,count = 100,result_type="recent",include_entities=True,tweet_mode='extended').pages(100)

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

        time.sleep(15*60)

    tweets.close()
    retweets.close()
    hts.close()
    ments.close()
    links.close()
