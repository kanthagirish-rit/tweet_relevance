"""
python version:3.5
"""

__author__ = "Kantha Girish", "Pankaj Uchil Vasant", "Samana Katti"

from os import listdir
from os.path import isdir, isfile, join

from naivebayes import NaiveBayes
from util import config, getLogger

logger = getLogger("train_classifiers")


def getData(folder):
    """
    :param folder: full path of the folder read files from for training the model
    :return: documents(list of documents), labels(list of labels)

    This function will put all the contents of the documents in each category into a list
    and creates a list of labels which are the names of the category folders
    """
    data = {}
    for f in listdir(folder):
        if isdir(join(folder, f)):
            data[f] = []
            for file in listdir(join(folder, f)):
                if isfile(join(folder, f, file)) and ".txt" in file:
                    with open(join(folder, f, file)) as fobj:
                        data[f].append(fobj.read().replace('\n', ''))
    documents = []
    labels = []
    debugStr = ""
    for key in data:
        debugStr += "folder: " + key + ", files: " + str(len(data[key])) + "\n"
        documents.extend(data[key])
        labels.extend([key]*len(data[key]))
    logger.debug(debugStr)
    return documents, labels


def trainTrendClassifier():
    """
    :return: None

    This function instantiates a model of the NaiveBayes class and trains the model on the
    categorized trends data. The trained model is stored in the database for future
    classification purpose.
    """
    logger.debug("trainTrendsClassifier()")
    trainingFolder = config['training']['trends']
    trainingDocs, trainingLabels = getData(trainingFolder)
    logger.debug("documents: " + str(len(trainingDocs)) +
                 ", labels: " + str(len(trainingLabels)))

    model = NaiveBayes()

    model.train(trainingDocs, trainingLabels, stopWordsFlag=True, stem=True)
    model.saveToDB()


def main():
    """
    :return: None

    runs all the functions for main script.
    """
    trainTrendClassifier()

if __name__ == '__main__':
    main()