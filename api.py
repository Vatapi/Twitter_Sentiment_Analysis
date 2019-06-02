from tweepy import OAuthHandler
import tweepy

#consumer key, consumer secret, access token, access secret.
consumer_key="3ssugLcD9o77dRyZCveWQQW4z"
consumer_secret="Hy5vKHVd4SBDqQGOs0hP5BYFLAJQWwsFR5MVW4M0Fvksu3XiTw"
access_token="1134726781217284096-n3loG4HSo94tIVEQot1OGUkRcqPPXf"
access_secret="ScFCe0A8au14geQdwTnAamCH6smH8GJs7JiJuVOy2gLla"

auth = OAuthHandler(consumer_key , consumer_secret)
auth.set_access_token(access_token , access_secret)
api = tweepy.API(auth)

def BuidTestSet(query):
    lang = 'en'
    max_tweets = 200
    tweets_fetched = []
    for tweet in tweepy.Cursor(api.search,q=query,lang=lang , tweet_mode = 'extended').items(max_tweets):
        tweets_fetched.append({'text':tweet._json['full_text'] , 'label':None})
        # print(tweet)
        # print(tweet._json['full_text'])
        # print()
    return tweets_fetched

#Tseting the Test Set
# Testdataset = BuidTestSet(query="SAvBAN")
# for item in Testdataset[0:4]:
#     print(item['text'])
#     print(item['label'])
#     print()



def BuildTrainingSet(corpusfile , tweetdatafile):
    import csv
    import time

    corpus = []
    with open(corpusfile , 'r') as csvfile:
        file = csv.reader(csvfile , delimiter=',' , quotechar = "\"")
        for row in file:
            corpus.append({'tweet_id':row[2] , 'label':row[1] , 'topic':row[0]})

    TrainingSet = []
    counnt = 0

    rate_limit = 180
    sleep_time = 900/180
    
    for tweet in corpus:
        try:
            status = api.get_status(tweet['tweet_id'] , tweet_mode='extended')
            counnt += 1
            print("tweet_fetched  " + status.full_text + "  " + counnt)
            tweet['text'] = status.full_text
            TrainingSet.append(tweet)
            time.sleep(sleep_time)
        except:
            print("Tweet Could Not Be Fetched")
            continue

    with open(tweetdatafile , 'w') as csvfile:
        writer = csv.writer(csvfile , delimiter = ',' , quotechar= "\"")
        for tweet in TrainingSet:
            try:
                writer.writerow([tweet["tweet_id"], tweet["text"], tweet["label"], tweet["topic"]])
            except Exception as e:
                print(e)

    return TrainingSet

corpusfile = 'C:\\Users\Bharat\Desktop\Twitter Sentiment Analysis\corpus.csv'
tweetdatafile = "C:\\Users\Bharat\Desktop\Twitter Sentiment Analysis\\tweet_training_set.csv"

BuildTrainingSet(corpusfile , tweetdatafile)
