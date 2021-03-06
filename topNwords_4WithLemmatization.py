__author__ = 'Snehal'

# ----------------------------------------------------------------------------------------------------------------------
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from nltk.classify import MaxentClassifier
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import string

# ----------------------------------------------------------------------------------------------------------------------
lmtzr = WordNetLemmatizer()
# lmtzr.lemmatize('cars')

# Print the classification of the problem
print ' Maximum Entropy classifier with lemmatization: '

all_words = nltk.FreqDist(word for word in movie_reviews.words())
top_words = set(all_words.keys()[:1000])

print(all_words.__len__())
print(top_words.__len__())

def word_feats(words):
    return dict([(lmtzr.lemmatize(word), True) for word in top_words and words ])

#
# def word_feats(words):
#     return {word:True for word in words if word in top_words and words}

# Get all the reviews with negative dataset and positive dataset from the movie reviews.
negids = movie_reviews.fileids('neg')
posids = movie_reviews.fileids('pos')


# Mark the word in the dataset as positive and negative.
negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

# Set some cut off for separating the training data and testing data.
negcutoff = len(negfeats)*25/100
poscutoff = len(posfeats)*25/100

# Based on the cut off, fill the training data and testing data with its respective positive and negative dataset.
trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

# Call Maximum Entropy Classifier to classify the training data.
algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
classifier = nltk.MaxentClassifier.train(trainfeats, algorithm,max_iter=3)
classifier.show_most_informative_features(10)

# Print the accuracy of the algorithm.
print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
# classifier.show_most_informative_features()


# algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
# classifier = nltk.MaxentClassifier.train(trainfeats, algorithm, max_iter=3)
# print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
# --------------------------------------------------------------------------

