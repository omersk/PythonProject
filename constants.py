# This is a constant file that organize all the
# constants in the python files of the project
"""
Name_Of_The_Project - Smads (Smart Ads)
Name_Of_The_Programmer - Omer Sasoni
Version - 6.0
Helped - Eldad Kapitolnik and Ori Levi
"""

# Email Constants

DEFAULT_CONTENT = 'example email stuff here'
HOST = 'smtp.gmail.com'
PORT = 587
EMAIL = 'freeadsandspam@gmail.com'
PASSWORD = 'toocoolforschool'
CUSTOMERS = []
SUBJECTS = ['new ad were found', 'ad were found by SMADS', 'best ad for you']
COMMASPACE = ', '
BLOCKED_CUSTOMERS = ["ofir200066@gmail.com", "yitay2010@gmail.com",
                     "ilanitks@walla.com"]
SEND_EMAIL_MASSAGE = 'an email has been sent to you'

# Getting History

OUTPUT_FILE_PATH = 'C:\search_logger.txt'
COPY_OF_THE_HISTORY_PATH = 'C:\history'
NEW_OUTPUT_FILE_PATH = 'C:\last_search_logger.txt'
HISTORY_PATH = r"\\AppData\Local\Google\Chrome\User Data\Default\History"

# PhantomJs And Ads Finding

PHANTOM_JS_PATH = 'C:\phantomjs-2.1.1-windows\\bin\phantomjs.exe'
OUTPUT_AD_PATH = 'ad.png'
DEFAULT_WINDOW_SIZE = (1024, 768)
AD_DATABASE = 'https://www.findads.com.au/pets-animals/b.html?usp=true'
KEYWORD_BUTTON_XPATH = '//*[@id="txtSearch"]'
SEARCH_BUTTON_XPATH = '/html/body/header/div/div[1]/form/button'
AD_XPATH = '/html/body/div[1]/section/div/div[1]/div[4]/div[1]/div[1]/' \
           'section[1]'
COMPARE_ELEMENT_XPATH = '//*[@id="fSearch"]'
CATAGORY_SORT_XPATH = '/html/body/div[1]/section/div/div[1]/div[5]/div/' \
                      'div[3]/form/div[1]/div[1]'
NAME_OF_THE_IMAGE = 'TheImage.png'

# Banned Words

BAD_WORDS = 'anal,anus,arse,ass,ballsack,balls,bastard,bitch,biatch,' \
            'bloody,blowjob,blow job,bollock,bollok,boner,boob,' \
            'bugger,bum,butt,buttplug,clitoris,cock,coon,crap,cunt,' \
            'damn,dick,dildo,dyke,fag,feck,fellate,fellatio,felching,' \
            'fuck,f u c k,fudgepacker,fudge packer,flange,Goddamn,God ' \
            'damn,hell,homo,jerk,jizz,knobend,knob end,labia,lmao,lmfao,' \
            'muff,nigger,nigga,omg,penis,piss,poop,prick,pube,pussy,queer,' \
            'scrotum,sex,shit,s hit,sh1t,slut,smegma,spunk,tit,tosser,' \
            'turd,twat,vagina,wank,whore,wtf'
BAD_WORDS = BAD_WORDS.split(',')
# Algorithm To Find The Best Word

MU = 0
VARIANCE = 1612180490515.47

# Regex To Find The Searches

REGEX = r"https:\/\/www\.google\.co\.il\/search\?q=(.*)&rlz." \
        r"*(\d\d\d\d-\d\d-\d\d \d\d:\d\d\:\d\d\.\d\d\d\d\d\d)|" \
        r"https:\/\/www.google.co.il\/search\?.*q=(.*?)&.*(\d\d" \
        r"\d\d-\d\d-\d\d \d\d:\d\d\:\d\d\.\d\d\d\d\d\d)"

# Chrome Passwords:

LOCAL_APP_DATA = 'localappdata'
PATH_TO_PASSWORDS = '\\Google\\Chrome\\User Data\\Default\\'
LOGIN_DATA = "Login Data"
EXECUTE = 'SELECT action_url, username_value, password_value FROM logins'
UNICODE_NORMALIZED = 'NFKD'
ENCODE = 'ascii', 'ignore'
ERRORS = ['database is locked',
          'no such table: logins',
          'unable to open database file']
# Sleep Time

SLEEP_TIME = 86400  # Day in seconds
