import pandas as pd

path = r"C:\\Users\\Matthew Osborne\\Documents\\python_code\\GeneHackMen\\"

BinnedFile = r"Data\\PittsburghData\\PittsburghBinCounts.csv"
TweetFile = r"Data\\PittsburghData\\PittsburghRounded.csv"

Binned = pd.read_csv(path + BinnedFile)
Tweets = pd.read_csv(path + TweetFile)
length = 20
NumIntervals = len(Binned)//length

MaxIndex = []
Maxes = []

for i in range(NumIntervals):
	Subset = Binned['NumTweets'][i*length:(i+1)*length]
	max = Subset.max()
	ind = Subset[Subset == max].index.values[0]

	MaxIndex.append(ind)
	Maxes.append(max)

del max
del ind
del Subset
del length
del NumIntervals

MaxTime = []
for index in MaxIndex:
	MaxTime.append(Binned['Time'][index])

URLs = []

for time in MaxTime:
	TimeDF = Tweets.loc[Tweets.Time == time,]
	TopRT = TimeDF.loc[TimeDF.Retweet_Count == max(TimeDF.Retweet_Count),'TweetID'].values[0]


	URLs.append(str(TopRT))

ForDF = []

for i in range(len(URLs)):
	ForDF.append((MaxTime[i],Maxes[i],URLs[i]))

DF = pd.DataFrame(ForDF,columns = ['Time','NumTweets','TweetID'])
DF.to_csv(path + r"Data\\PittsburghData\\RetweetsForHTML.csv",index=False)
