import re
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords

class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT-USER' , "URL"])

    def processtweets(self , tweet):
        tweet = tweet.lower()
        tweet = re.sub( '((www.[^\s]+) | (https?://[^\s]+) | (http?://[^\s]+))' , 'URL' , tweet)
        tweet = re.sub( '(@[^\s]+)' , 'AT_USER' , tweet)
        tweet = re.sub( r'#([^\s]+)' , r'\1' , tweet)
        tweet = word_tokenize(tweet)
        for word in tweet:
            if word not in self._stopwords:
                return word

    def processedtweets(self , list_of_tweets):
        processed_tweets = []
        for tweet in list_of_tweets:
            pTweet = self.processtweets(tweet['text'])
            processed_tweets.append(pTweet , tweet['label'])

        return processed_tweets
