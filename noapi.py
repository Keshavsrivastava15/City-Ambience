import snscrape.modules.twitter as sntwitter
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
obj = SentimentIntensityAnalyzer()
import pandas as pd
import pickle
import sys


query = "kolkata min_faves:5 lang:en until:2022-12-24 since:2022-12-18"
# bangalore news lang:en until:2022-11-01 since:2022-10-01 -filter:links -filter:replies
tweets = []
limit =  3000
column=['Time','Tweet','Analysis']

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    
    if len(tweets) == limit:
        break
    else:
        sentiment_dict = obj.polarity_scores(tweet.content)
        tweets.append([tweet.date.strftime("%m/%d/%Y, %H:%M:%S"),tweet.content,sentiment_dict['compound']])
        
df = pd.DataFrame(tweets, columns=column)
print(df)

df.to_csv('kolkata1.csv')