from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys

#Main Class of the BOT
class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        #This is For Finding the Right Text Box and Logging the User In
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(2)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(2)

        #Function to Like the Images and Videos on the Page
    def like_photo(self, hashtag):
        driver = self.driver
        time.sleep(1)
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(1)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 2):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                #Getting the Link Tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                #Finding the Unique Image Link
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                #Building the List
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        file = open('links.txt','a')
        file.write(str(pic_hrefs))

        #Function to Like the Images from the URL
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(2, 4))
                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]')
                like_button().click()
                time.sleep(1)
            except Exception as e:
                time.sleep(2)
            unique_photos -= 1

#User Credits
#Your Data in Local
username = "USERNAME"
password = "PASSWORD"

ig = InstagramBot(username, password)
ig.login()
#You Can Sepcify your Own HashTags
hashtags = ['music','cars','programming','code']

while True:
    tag = random.choice(hashtags)
    ig.like_photo(tag)
    
