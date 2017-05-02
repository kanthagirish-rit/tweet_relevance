"""
file: vsm.py
python version: 3.5
description: Vector space modelling
"""

import math
import re
from collections import Counter

WORD = re.compile(r'\w+')


class Vsm:
    """
    """
    __slots__ = ["documents", "termList", "docLists", "docLength"]

    def __init__(self, documents):
        self.documents = documents
        self.termList = []
        self.docLists = []
        self.docLength = [0]*len(documents)

        for i in range(len(self.documents)):
            words = self.documents[i].split()

            for word in words:
                if word not in self.termList:
                    self.termList.append(word)
                    self.docLists.append([Document(i, 1)])
                else:
                    index = self.termList.index(word)
                    docList = self.docLists[index]

                    match = False
                    for doc in docList:
                        if doc.id == i:
                            doc.weight += 1
                            match = True
                            break
                    if not match:
                        docList.append([Document(i, 1)])

        n = len(self.documents)
        for docList in self.docLists:
            df = len(docList)
            for doc in docList:
                tfidf = (1 + math.log2(doc.weight)) * math.log2(n/df)
                doc.weight = tfidf
                self.docLength[doc.id] += tfidf ** 2

        self.docLength = [math.sqrt(x) for x in self.docLength]

    def rankSearch(self, query, returnTop=5):
        """
        :param query:
        :param returnTop:
        :return:
        """
        docs = {}


class Document:
    """
    """
    __slots__ = ["id", "weight"]

    def __init__(self, id, weight):
        self.id = id
        self.weight = weight


def getSimilarity(string1, string2):
    """
    :param string1:
    :param string2:
    :return:
    """
    vector1 = _sentenceToVector(string1)
    vector2 = _sentenceToVector(string2)

    intersection = set(vector1.keys()) & set(vector2.keys())
    tfidf = sum([vector1[word]*vector2[word] for word in intersection])
    norm1 = sum([value**2 for value in vector1.values()])
    norm2 = sum([value ** 2 for value in vector2.values()])
    normalizingFactor = math.sqrt(norm1) * math.sqrt(norm2)

    if not normalizingFactor:
        return 0.0
    else:
        return tfidf / normalizingFactor


def _sentenceToVector(sentence):
    words = WORD.findall(sentence)
    return Counter(words)