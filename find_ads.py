"""
Name_Of_The_Project - Smads (Smart Ads)
Name_Of_The_Programmer - Omer Sasoni
Version - 6.0
Helped - Eldad Kapitolnik and Ori Levi
"""
from selenium import webdriver, common
from PIL import Image
import constants
import operator
import os
import zipfile


class PhantomJsDriver:
    """
    A class that taking care on the ads finding
    in the internet, doing it with PhantomJs -
    background driver
    """
    def __init__(self, ad_keyword, window_size=constants.DEFAULT_WINDOW_SIZE,
                 panthom_js_path=constants.PHANTOM_JS_PATH,
                 output_ad_path=constants.OUTPUT_AD_PATH):
        """
        this function init our object
        in order to use the other functions
        that the object offer.

        Parameters
        ----------
        phantom_js_path : str
            path of the PhantomJs ( this essential because
            we cannot get the PhantomJs file otherwise)
        output_ad_path : str
            where you want to save the ad that the system
            had found and how you call the name of the ad
            file ( eg: ad.png )
        ad_keyword : str
            the keyword that define what ad the system bring
            ( eg: dog will bring dog ad )
        window_size : double int (int1,int2)
            define the window size of the browser ( mainly for the
            screenshot )
        """
        self.phantom_js_path = panthom_js_path
        self.output_ad_path = output_ad_path
        self.ad_keyword = ad_keyword
        self.window_size = window_size
        self.list_of_images = []
        self.dict = {}
        self.element = True

    def get_ad(self):
        """
        this function save the ad by searching in the internet
        ( on specific website ) the keyword that the user chose
        and copy it into the output_ad_path.

        Parameters
        ----------

        None
        """
        driver = webdriver.PhantomJS(self.phantom_js_path)
        driver.set_window_size(self.window_size[0], self.window_size[1])
        for i in range(0, 5):
            # we do it 5 times in order to choose the best ad crop
            driver.get(constants.AD_DATABASE)
            kwd = driver.find_element_by_xpath(
                constants.KEYWORD_BUTTON_XPATH)
            kwd.send_keys(self.ad_keyword)
            search_button = driver.find_element_by_xpath(
                constants.SEARCH_BUTTON_XPATH)
            search_button.click()
            driver.save_screenshot("ad" + str(i) + ".png")
            try:
                element = driver.find_element_by_xpath(constants.AD_XPATH)
                # find part of the page you want image of
                self.crop_image(i, element)
            except common.exceptions.NoSuchElementException:
                self.element = False

    def crop_image(self, i, ad_element):
        """
        this function crop the screenshot of the ads website from
        the previous function into one single ad.

        Parameters
        ----------

        i : int
            the number of the search.

        ad_element : selenium.webdriver.remote.webelement.WebElement
            the element of the ad in the web.
        """
        im = Image.open("ad" + str(i) + ".png")
        # uses PIL library to open image in memory
        location = ad_element.location  # the location of the element
        size = ad_element.size
        left = location['x'] + 50
        top = location['y']
        right = location['x'] + size['width'] + 50
        bottom = location['y'] + size['height']
        im = im.crop((left, top, right, bottom))  # defines crop points
        im.save('test' + str(i) + '.png')  # saves new cropped image
        self.list_of_images.append('test' + str(i) + '.png')
        self.dict['test' + str(i) + '.png'] = 0

    def choose_the_best_ad(self):
        """
        this function choose the most common ad file in order
        to avoid random problems ( done because of problems in
        the test phase ) .

        Parameters
        ----------
        None
        """
        for img1 in self.list_of_images:
            for img2 in self.list_of_images:
                im1 = Image.open(img1)
                im2 = Image.open(img2)

                if list(im1.getdata()) == list(im2.getdata()):
                    # meaning if they equal
                    self.dict[img1] += 1
                    self.dict[img2] += 1
        BestImage = max(self.dict.iteritems(), key=operator.itemgetter(1))[0]
        # choose the most common picture
        if os.path.exists(constants.NAME_OF_THE_IMAGE):
            # remove the last chosen ad
            os.remove(constants.NAME_OF_THE_IMAGE)

        os.rename(BestImage, constants.NAME_OF_THE_IMAGE)
        zipf = zipfile.ZipFile('Pictures_Of_The_Search.zip', 'w',
                               zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(os.curdir):
            for file in files:
                if (file[0:2] == 'ad' or file[0:4] == 'test') and\
                                file[-3:] == 'png':
                    zipf.write(os.path.join(root, file))
                    os.remove(file)
