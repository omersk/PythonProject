# coding=utf8
# the above tag defines encoding for this
# document and is for Python 2.x compatibility
"""
Name_Of_The_Project - Smads (Smart Ads)
Name_Of_The_Programmer - Omer Sasoni
Version - 6.0
Helped - Eldad Kapitolnik and Ori Levi
"""
import sys
import urllib
import re
import constants


class QueryFinder(object):
    """
    this class takes as an input regex
    and filters out the words that are
    appropriate for regex.
    In our use we would take the query
    of the searches in the history search.
    """
    def __init__(self, regex, input_file_path, output_file_path):
        """
        this function init our object
        in order to use the other functions
        that the object offer.

        Parameters
        ----------
        regex : str
            the regex that we will use on
            the file in order to find the
            queries ( in our case )
        input_file_path : str
            the file path that we will use
            the regex on him
        output_file_path : str
            the file that we will save our
            queries there
        """
        self.regex = regex
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path

    def find_queries(self):
        """
        this function runs the regex on
        the text file and extracts the queries

        Parameters
        ----------
        None
        """

        f = open(self.input_file_path, 'r')
        test_str = f.read()
        oldstdout = sys.stdout
        sys.stdout = open(self.output_file_path, 'w')
        matches = re.finditer(self.regex, test_str)
        isnt_hebrew = 0
        for matchNum, match in enumerate(matches):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                isnt_hebrew -= 1
                if urllib.unquote_plus(
                        urllib.unquote_plus("{group}".format(
                                group=match.group(groupNum)))) != "None":
                    # if '%D' not in match.group(groupNum) and isnt_hebrew < 0:
                    print urllib.unquote_plus(
                        urllib.unquote_plus("{group}".format(
                            group=match.group(groupNum))))
                    # elif '%D' not in match.group(groupNum):
                    # isnt_hebrew = 1
        sys.stdout = oldstdout
