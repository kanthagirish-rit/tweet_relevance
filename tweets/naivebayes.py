"""
python version:3.5
"""

__author__ = "Kantha Girish", "Pankaj Uchil Vasant", "Samana Katti"

import numpy as np
from nltk.stem import PorterStemmer
from collections import Counter
import re
import datetime

from database import getDBInstance
from util import getStopwords
from util import getLogger


WORD = re.compile(r'[\s.(),-:?\"$]')
logger = getLogger("train_classifiers.NaiveBayes")


class NaiveBayes:
    """
    """
    __slots__ = ["documents", "labels", "numClasses", "classes", "vocabulary", "classTokens",
                 "condProbs", "classCounts", "stemmer", "stopWords", "stem", "numWords",
                 "numDocuments"]

    def __init__(self):
        self.documents = None
        self.labels = None
        self.classes = None
        self.numClasses = None
        self.vocabulary = []
        self.classTokens = None
        self.condProbs = None
        self.classCounts = None
        self.stemmer = PorterStemmer()
        self.stopWords = True
        self.numWords = None
        self.stem = False
        self.numDocuments = 0

    def loadModelFromDB(self):
        """
        :return: None

        This method loads a pre-trained model from the database if it exists for trend
        classification.
        """
        db = getDBInstance()
        modelObject = db.models.find_one({"type": "nb_trends"})

        if modelObject:
            logger.debug("loadModelFromDB() loaded model successfully")
            model = modelObject["model"]

            self.classes = model["classes"]
            self.numClasses = model["numClasses"]
            self.vocabulary = model["vocabulary"]
            self.classTokens = model["classTokens"]
            self.condProbs = model["condProbs"]
            self.classCounts = model["classCounts"]
            self.stopWords = model["stopWords"]
            self.numWords = model["numWords"]
            self.stem = model["stem"]
            self.numDocuments = model["numDocuments"]
        else:
            logger.debug("No model found in DB. Please train a new model.")

    def train(self, documents, labels, stopWordsFlag=True, numWords=None, stem=True):
        """
        :param stopWordsFlag: True/False, default True. Indicate whether to remove stopwords
            from the documents.
        :param documents: python list of documents as strings
        :param labels: python list of the categories such that label[i] corresponds to
            documents[i]
        :param numWords: Number of top repeated most common words to use for training.
            Default None - retains all the words.
        :param stem: True/False, default True. Indicate whether to stem the word in the
            document.
        :return: None

        This method trains the model on the documents and labels provided and creates
        conditional probabilities.
        """
        self.documents = documents
        self.numDocuments = len(documents)
        self.labels = labels
        self.classes = np.unique(labels)
        self.numClasses = self.classes.size
        self.classTokens = [0] * self.numClasses
        self.condProbs = [dict() for _ in range(self.numClasses)]
        self.classCounts = [0] * self.numClasses
        self.stem = stem
        self.stopWords = stopWordsFlag

        logger.debug("train() Training...")
        stopwords = getStopwords()
        for i in range(len(self.classes)):
            self.classCounts[i] = self.labels.count(self.classes[i])

        for i in range(self.numClasses):
            classStrings = " ".join([self.documents[k] for k in range(len(self.labels))
                                    if self.labels[k] == self.classes[i]])
            tokens = WORD.split(classStrings)
            counter = Counter(tokens)

            if numWords is None or numWords > len(counter):
                numWords = len(counter)
            self.numWords = numWords
            condProbs = dict(counter.most_common(numWords))

            # remove stop words
            if stopWordsFlag:
                removeList = []
                for token in condProbs:
                    if token in stopwords:
                        removeList.append(token)
                for token in removeList:
                    del condProbs[token]

            if stem:
                for token in condProbs:
                    stemmed = self.stemmer.stem(token)
                    if stemmed in self.condProbs[i]:
                        self.condProbs[i][stemmed] += condProbs[token]
                    else:
                        self.condProbs[i][stemmed] = condProbs[token]
            else:
                self.condProbs[i] = condProbs

            self.classTokens[i] += sum(self.condProbs[i].values())
            self.vocabulary.extend(self.condProbs[i].keys())

        for i in range(self.numClasses):
            for token in self.condProbs[i]:
                self.condProbs[i][token] = (self.condProbs[i][token] + 1) / \
                                           (self.classTokens[i] + len(self.vocabulary))

        predLabels = self.classifyAll(self.documents)
        accuracy = self.accuracy(self.labels, predLabels)
        logger.debug("Trained Naive Bayes with training accuracy: "
                     + str(np.round(accuracy*100, 2)) + "%")

    def classifyAll(self, documents):
        """
        :param documents: python list of documents as strings which are to be classified.
        :return: Predicted labels for the documents

        This method returns predicted class labels for the documents
        """
        labels = [0] * len(documents)

        logger.debug("classify() Running predictions: ")
        for idx in range(len(documents)):
            labels[idx] = self.classify(documents[idx])
        print("classify() Done")
        return labels

    def classify(self, document):
        """
        :param document: a string document to be classified.
        :return: Predicted label for the document.

        This method returns predicted class label for the document.
        """
        stopwords = getStopwords()
        score = np.zeros(shape=(self.numClasses, 1))
        for i in range(self.numClasses):
            score[i] = np.log(self.classCounts[i] / self.numDocuments)
        tokens = WORD.split(document)

        for i in range(self.numClasses):
            for token in tokens:
                if self.stopWords and token in stopwords:
                    continue
                if self.stem:
                    token = self.stemmer.stem(token)
                if token in self.condProbs[i]:
                    score[i] += np.log(self.condProbs[i][token])
                else:
                    score[i] += np.log(1 / (self.classTokens[i] + len(self.vocabulary)))

        classIndex = np.argmax(score)
        return self.classes[classIndex]

    def accuracy(self, targets, predictions):
        """
        :param targets: python list of target labels
        :param predictions: python list of predicted labels
        :return: Classification accuracy

        This method calculates the classification accuracy for the predictions and returns it.
        """

        actuals = dict(Counter(targets))
        logger.debug("accuracy()")
        counts = {}
        for idx in range(len(targets)):
            if targets[idx] in counts:
                if targets[idx] == predictions[idx]:
                    counts[targets[idx]] += 1
            else:
                if targets[idx] == predictions[idx]:
                    counts[targets[idx]] = 1
        for key in counts:
            logger.debug(key + ": " + str(round(counts[key]*100/actuals[key], 2)) + "%")
        return sum(counts.values())/sum(actuals.values())

    def saveToDB(self):
        """
        :return: None

        This method saves the trained model to database.
        """
        modelObject = {
            "classes": list(self.classes),
            "numClasses": self.numClasses,
            "vocabulary": self.vocabulary,
            "classTokens": self.classTokens,
            "condProbs": self.condProbs,
            "classCounts": self.classCounts,
            "stopWords": self.stopWords,
            "numWords": self.numWords,
            "stem": self.stem,
            "numDocuments": self.numDocuments
        }

        db = getDBInstance()
        logger.debug('saveToDB() before writing')

        db.models.update_one({
                "type": "nb_trends"
            }, update={
                "$set": {
                    "model": modelObject,
                    "updated": datetime.datetime.now()
                }
            }, upsert=True
        )
        logger.debug('saveToDB() model saved')