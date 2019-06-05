from TSA_preprocess import PreProcessTweets
import pandas as pd
from api import TestDataSet

TrainingData = pd.read_csv('tweet_training_set.csv' , encoding='unicode_escape')
TrainingData.columns = ['id' , 'text' , 'label' , 'topic']
test = TestDataSet(query='narendramodi')
TestData = test.buildTestSet()
# for item in TestData[0:4]:
    # print(item)
    # print(item[2])
    # print()

# print(len(TrainingData))
# print(list(row for row in TrainingData[:4].values))
tweet_processor = PreProcessTweets()
processedTrainingSet = tweet_processor.processedtweets(TrainingData.values)
processedTestSet = tweet_processor.processedtweets(TestData)
print(processedTrainingSet[:4])
print()
print("*********************************************************************************************************************************************************")
print()
print(processedTestSet[:4])
print()

#Build Vocabulary
import nltk

def BuildVocab(TrainingDataSet):
    all_words = []
    for (words, label) in TrainingDataSet:
        all_words.extend(words)

    wordlist =  nltk.FreqDist(all_words)
    word_features = wordlist.keys() #no. of occurences is the key
    return word_features

def extractFeatures(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in tweet_words:
        features['contains(%s)' % word] = (word in tweet_words)

    return features

word_features = BuildVocab(processedTrainingSet)
trainingFeatures = nltk.classify.apply_features(extractFeatures , processedTrainingSet)

NaiveBayesClassifier = nltk.NaiveBayesClassifier.train(trainingFeatures)

NaiveBayesLabels = [NaiveBayesClassifier.classify(extractFeatures(tweet[0])) for tweet in processedTestSet]

positive = NaiveBayesLabels.count('positive')
negaitve = NaiveBayesLabels.count('negative')
if positive > negaitve:
    print('Overall Positive Sentiment')
    print('Positive Sentiment Percentage = ' + str(100 * positive/(positive+negaitve)) )
else:
    print('Overall Negaitve Sentiment')
    print('Negaitve Sentiment Percentage = ' + str(100 * negaitve/(positive+negaitve)) )
