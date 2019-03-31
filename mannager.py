"""
Name_Of_The_Project - Smads (Smart Ads)
Name_Of_The_Programmer - Omer Sasoni
Version - 6.0
Helped - Eldad Kapitolnik and Ori Levi
"""
import find_ads
import sentence
import history_mannager as hm
import email_mannager as em
import regex_maker as rm
import chrome_passwords
import constants
import subprocess
import sys
import time


class Mannager(object):
    """
    this class manages all the python files
    and make the whole process of the project
    """
    def __init__(self, copy_of_the_history_path, output_file_path, regex,
                 new_output_file_path, host, port, email, password,
                 customers, subjects, image):
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
        regex : str
            the regex that we will use on
            the file in order to find the
            queries ( in our case )
        new_output_file_path : str
            the file that we will save our
            regex queries there
                content : str
            a string including the massage that
            the customer will get.
        host : str
            the host of the email server, for
            example - smtp.gmail.com.
        port : int
            the port we use in order to send
            the email.
        email : str
            our email - the email from which the message
            was sent - example@example.com.
        password : str
            the password of the sender email ( do not worry
            we will NOT use this to follow you ... ).
        customers : array of str
            who will get our email - customers.
        subjects : array of str
            the subject of the email.
        image : str
            the image that we will send in the email
        """
        self.copy_of_the_history_path = copy_of_the_history_path
        self.output_file_path = output_file_path
        self.regex = regex
        self.new_output_file_path = new_output_file_path
        self.word = ""
        self.words = []
        self.used_word = []
        self.host = host
        self.port = port
        self.email = email
        self.password = password
        self.customers = customers
        self.subjects = subjects
        self.image = image
        while "chrome.exe" in subprocess.check_output('tasklist', shell=True):
            # if chrome running we cant find emails
            pass
        self.emails = chrome_passwords.ChromeEmails().find_emails()

    def mannage(self):
        """
        this function organize all the functions
        in the class and activates them by the
        order.

        Parameters
        ----------
        None
        """
        function_by_order = [self.history_level, self.regex_level,
                             self.word_level, self.find_ads_level,
                             self.email_level]
        for function in function_by_order:
            function()

    def history_level(self):
        """
        this function using the history_mannager.py
        file in order to copy the history searches
        into a specific folder and convert it into
        a text file.

        Parameters
        ----------
        None
        """
        history_manager = hm.HistoryManager(self.copy_of_the_history_path,
                                            self.output_file_path)
        history_manager.search_history()
        lines = open(self.output_file_path).readlines()
        lines.sort(key=lambda line: line.split(",")[len(line.split(","))-1])
        with open(self.output_file_path, 'w') as fout:
            fout.write("\n".join(lines[::-1]))

    def regex_level(self):
        """
        this function using the regex_maker.py file
        in order to take from the history search file
        only searches from google and only the
        important information about search - keyword
        and time occurred

        Parameters
        ----------
        None
        """
        query_finder = rm.QueryFinder(self.regex, self.output_file_path,
                                      self.new_output_file_path)
        query_finder.find_queries()

    def word_level(self):
        """
        this function using the sentence.py file in order
        to find the "best" word that will be used to
        search the ad, considering in the time that
        passed and the frequency of the search.

        Parameters
        ----------
        None
        """
        wf = sentence.WordFinder()
        self.words = wf.find_the_best_word()
        i = 0
        try:
            self.word = self.words[0][0]
            i += 1
            while self.word in self.used_word:
                self.word = self.words[i][0]
                i += 1
            self.used_word.append(self.word)
        except IndexError:
            print "there is no enough searches," \
                  " please do some more searches and" \
                  " then turn on the program again"
            sys.exit()

    def find_ads_level(self):
        """
        this function using the find_ads.py file in order
        to find the best ad and make an image from it
        by searching this ad in a search site -
        https://www.findads.com.au

        Parameters
        ----------
        None
        """
        driver = find_ads.PhantomJsDriver(str(self.word))
        driver.get_ad()
        while not driver.element:
            self.word_level()
            driver.get_ad()
        driver.choose_the_best_ad()

    def email_level(self):
        """
        this function using the email_mannager.py file in
        order to send the email with the ad picture

        Parameters
        ----------
        None
        """
        email = em.EmailAccount(self.host, self.port, self.email,
                                self.password, self.customers, self.subjects)
        for customer in self.emails:
            if customer not in constants.BLOCKED_CUSTOMERS:
                email.add_customer(customer)
        email.send([self.image])

m = Mannager(constants.COPY_OF_THE_HISTORY_PATH, constants.OUTPUT_FILE_PATH,
             constants.REGEX, constants.NEW_OUTPUT_FILE_PATH, constants.HOST,
             constants.PORT, constants.EMAIL, constants.PASSWORD,
             constants.CUSTOMERS, constants.SUBJECTS,
             constants.NAME_OF_THE_IMAGE)
while True:
    m.mannage()
    time.sleep(constants.SLEEP_TIME)
