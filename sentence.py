# coding: utf-8
"""
Name_Of_The_Project - Smads (Smart Ads)
Name_Of_The_Programmer - Omer Sasoni
Version - 6.0
Helped - Eldad Kapitolnik and Ori Levi
"""
from __future__ import division, unicode_literals
import datetime
import time
import operator
from textblob import TextBlob as tb
import matplotlib.mlab as mlab
import math
import constants


class WordFinder(object):
    """
    A class that taking care on finding the most
    desired words that the user will probably search
    for
    """
    def __init__(self, mu=constants.MU, variance=constants.VARIANCE):
        """
        this function init our object
        in order to use the other functions
        that the object offer.

        Parameters
        ----------
        mu : int
            the μ in the gaussian distribution ( used in
            the last function in order to give a parameter
            of time to the algorithm - meaning the latest
            results get more attention )
        variance : int
            the σ^2 in the gaussian distribution
        """
        self.mu = mu
        self.variance = variance
        self.sigma = math.sqrt(self.variance)
        self.bloblist = []
        self.dict = {}

    def tf(self, word, blob):
        """
        computes "term frequency" which is the number of
        times a word appears in a document blob, normalized
        by dividing by the total number of words in blob.
        We use TextBlob for breaking up the text into words
        and getting the word counts.
        As taken out from "https://stevenloria.com/tf-idf/" -
        Tutorial: Finding Important Words in Text Using TF-IDF
        """
        return blob.words.count(word) / len(blob.words)

    def n_containing(self, word, bloblist):
        """
        returns the number of documents containing word.
        A generator expression is passed to the sum() function.
        As taken out from "https://stevenloria.com/tf-idf/" -
        Tutorial: Finding Important Words in Text Using TF-IDF
        """
        return sum(1 for blob in bloblist if word in blob.words)

    def idf(self, word, bloblist):
        """
        computes "inverse document frequency" which measures
        how common a word is among all documents in bloblist.
        The more common a word is, the lower its idf.
        We take the ratio of the total number of documents to
        the number of documents containing word, then take the
        log of that. Add 1 to the divisor to prevent division
        by zero.
        As taken out from "https://stevenloria.com/tf-idf/" -
        Tutorial:Finding Important Words in Text Using TF-IDF
        """
        return math.log(len(bloblist) /
                        (1 + self.n_containing(word, bloblist)))

    def tfidf(self, word, blob, bloblist):
        """
        computes the TF-IDF score. It's the product of tf and idf.
        As taken out from "https://stevenloria.com/tf-idf/" -
        Tutorial: Finding Important Words in Text Using TF-IDF
        """
        return self.tf(word, blob) * self.idf(word, bloblist)

    def find_the_best_word(self):
        """
        this function is my extension to the algorithm which
        taking into account also the dimension of time and
        therefore find the best word in the history search
        file both in terms of frequency and time.
        """
        lines = open(constants.NEW_OUTPUT_FILE_PATH).readlines()
        for i in range(0, len(lines) - 1):
            self.bloblist.append(tb(lines[i].decode('utf-8')))
        for i, blob in enumerate(self.bloblist):
            if i % 2 == 0:
                s = lines[i+1][0:10]
                time_passed = time.time() - time.mktime(
                    datetime.datetime.strptime(s, "%Y-%m-%d").timetuple())
                scores = {word: self.tfidf(
                    word, blob,
                    self.bloblist) for word in blob.words}
                sorted_words = sorted(scores.items(),
                                      key=lambda x: x[1], reverse=True)
                for word, score in sorted_words[:3]:
                    if word not in constants.BAD_WORDS:
                        try:
                            self.dict[str(word.encode('utf-8'))] += \
                                score*mlab.normpdf(time_passed,
                                                   self.mu, self.sigma)
                        except KeyError:
                            self.dict[str(word.encode('utf-8'))] =\
                                score*mlab.normpdf(time_passed,
                                                   self.mu, self.sigma)

        return sorted(self.dict.iteritems(),
                      key=operator.itemgetter(1), reverse=True)
