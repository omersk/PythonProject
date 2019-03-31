"""
Name_Of_The_Project - Smads (Smart Ads)
Name_Of_The_Programmer - Omer Sasoni
Version - 6.0
Helped - Eldad Kapitolnik and Ori Levi
"""
import smtplib
import constants
import random
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


class EmailAccount():
    """
    A class which taking care about all the
    action of sending ads to our customers
    """
    def __init__(self, host, port, email, password, customers, subjects):
        """
        this function init our object
        in order to use the other functions
        that the object offer.

        Parameters
        ----------
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
        password : string
            the password of the sender email ( do not worry
            we will NOT use this to follow you ... ).
        customers : array of str
            who will get our email - customers.
        subjects : array of str
            the subject of the email.
        """
        self.host = host
        self.port = port
        self.email = email
        self.password = password
        self.customers = customers
        self.subjects = subjects

    def add_customer(self, new_customer_email):
        """
        void function - checking if the customer is
        already in the list and adding him if not

        Parameters
        ----------
        new_customer_email : str
            the new customer email
        """
        if new_customer_email not in self.customers:
            self.customers.append(new_customer_email)

    def delete_customer(self, customer_email):
        """
        void function - checking if the customer is
        on the list and deleting him if he does

        Parameters
        ----------
        customer_email : str
            the customer email
        """
        if customer_email in self.customers:
            self.customers.remove(customer_email)

    def send(self, images):
        """
        sending our email to our customer via smtplib
        module.

        Parameters
        ----------
        content : str
            a string including the massage that
            the customer will get.
        """
        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = self.subjects[random.randint(0, len(self.subjects)-1)]
        msg['From'] = constants.EMAIL
        msg['To'] = constants.COMMASPACE.join(self.customers)
        msg.preamble = 'Hello, we have found ad for you :)'
        # Assume we know that the image files are all in PNG format
        for image in images:
            # Open the files in binary mode.
            # Let the MIMEImage class automatically
            # guess the specific image type.
            fp = open(image, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)
        # sending email :
        mail = smtplib.SMTP(self.host, self.port)
        mail.ehlo()
        mail.starttls()
        mail.login(self.email, self.password)
        mail.sendmail(self.email, self.customers, msg.as_string())
        print constants.SEND_EMAIL_MASSAGE
        mail.close()
