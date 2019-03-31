"""
Name_Of_The_Project - Smads (Smart Ads)
Name_Of_The_Programmer - Omer Sasoni
Version - 6.0
Helped - Eldad Kapitolnik and Ori Levi
"""
import csv
import sqlite3
import shutil
import os
import constants
from datetime import datetime, timedelta


class HistoryManager:
    """
    A class that taking care on the history
    searching ( for google chrome only )
    """
    def __init__(self, copy_of_the_history_path, output_file_path):
        """
        this function init our object
        in order to use the other functions
        that the object offer.

        Parameters
        ----------
        copy_of_the_history_path : str
            path of the file that will be a
            copy of the history search file
            of chrome ( this essential because
            we cannot get the chrome file otherwise)
        output_file_path : str
            where you want to save the history searching
        """
        self.user_profile = os.environ.get("USERPROFILE")
        self.encrypted_file_path = self.user_profile + constants.HISTORY_PATH
        self.copy_of_the_history_path = copy_of_the_history_path
        self.output_file_path = output_file_path

    def search_history(self):
        """
        this function read the copy
        of the history file
        file and write it in a normal
        way in the output_file

        Parameters
        ----------
        None
        """
        shutil.copyfile(self.encrypted_file_path,
                        self.copy_of_the_history_path)
        connection = sqlite3.connect(self.copy_of_the_history_path)
        connection.text_factory = str  # set the objects returned for text to str
        cur = connection.cursor()
        output_file = open(self.output_file_path, 'wb')
        csv_writer = csv.writer(output_file)
        headers = ('URL', 'Title', 'Visit Count', 'Date (GMT)')
        epoch = datetime(1601, 1, 1)
        csv_writer.writerow(headers)
        for row in (cur.execute('select url,last_visit_time from urls')):
            row = list(row)
            url_time = epoch + timedelta(microseconds=row[1])
            row[1] = url_time
            if '%D' not in row[0]:
                csv_writer.writerow(row)
