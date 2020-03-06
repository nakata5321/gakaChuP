from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys

from web_parser.hashfield import *

class HashTagParser:
    def __init__(self, driver_location = '/usr/bin/google-chrome-stable', headless=True):
        self.__chrome_options = webdriver.ChromeOptions()
        if(headless):
            self.__chrome_options.add_argument("--headless")
        self.__chrome_options.binary_location = driver_location
        self.__webDriver = webdriver.Chrome(options=self.__chrome_options)

    def signIn(self, name, password):
        self.__webDriver.get('https://www.instagram.com/accounts/login')
        time.sleep(1)
        username_place = self.__webDriver.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')
        password_place = self.__webDriver.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')
        login_button = self.__webDriver.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[4]/button')

        username_place.send_keys(name)
        password_place.send_keys(password)
        login_button.submit()
        time.sleep(2)

    def findHashtagsInPost(self, link):
        assert(link!=""),"[LINK ERROR] Given empty link"
        self.__webDriver.get(link)
        soup = BeautifulSoup(self.__webDriver.page_source,"lxml")
        desc = " "

        for item in soup.findAll('a'):
            desc= desc + " " + str(item.string)

        taglist = desc.split()
        taglist = [x for x in taglist if x.startswith('#')]

        for index in range(0,len(taglist)):
            taglist[index] = taglist[index].strip('#').lower()

        return taglist

    def getHashtagPostCount(self,hashtag):

        self.__webDriver.get('https://www.instagram.com/explore/tags/'+str(hashtag))
        soup = BeautifulSoup(self.__webDriver.page_source,"lxml")

        nposts_string = soup.find('span', {'class': 'g47SY'}).text
        nposts = int(nposts_string.replace(',', ''))
        return nposts

    def getLinksForTopPostsByHastag(self, hashtag, amount):
        li = []

        self.__webDriver.get('https://www.instagram.com/explore/tags/'+str(hashtag))
        soup = BeautifulSoup(self.__webDriver.page_source,"lxml")
        for j in range(0,int(amount/21)):
            for a in soup.find_all('a', href=True):
                li.append(a['href'])
            self.__webDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        links = ['https://www.instagram.com'+x for x in li if x.startswith('/p/')]
        return links

    def getLinksForUsersPosts(self, userlink, max_count=21):
        li = []

        self.__webDriver.get(userlink)
        soup = BeautifulSoup(self.__webDriver.page_source,"lxml")
        for j in range(0,int(max_count/21)):
            for a in soup.find_all('a', href=True):
                if a['href'] not in li:
                    li.append(a['href'])
            self.__webDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.3)
        time.sleep(1)
        links = ['https://www.instagram.com'+x for x in li if x.startswith('/p/')]
        return links

    def getPostLikers(self, postlink):
        self.__webDriver.get(postlink)
        self.__webDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        userid_element = self.__webDriver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[2]/section[2]/div/div/button').click()
        time.sleep(1)

        users = {}
        heightPage = self.__webDriver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/div").value_of_css_property("padding-top")
        match = False
        usersCount = 0
        while match==False:
            lastHeightPage = heightPage
            elements = self.__webDriver.find_elements_by_xpath("//*[@id]/div/a")
            for element in elements:
                if element.get_attribute('title') not in users.keys():

                    users[element.get_attribute('title')] = element.get_attribute('href')
                    # print(users)
                    usersCount+=1
                    print("Searching users:", usersCount)
        # #     # step 3
            self.__webDriver.execute_script("return arguments[0].scrollIntoView();", elements[-1])
            time.sleep(0.4)
        #
        #     # step 4
            heightPage = self.__webDriver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/div").value_of_css_property("padding-top")
            if lastHeightPage==heightPage:
                match = True

        return users

    def getHashTagMap(self, post_link, hashfield):
        f_hashtag_list = self.findHashtagsInPost(post_link)
        for h in f_hashtag_list:
            hashfield.addHashTag(h)
            hashfield.addRelHashTags(h, f_hashtag_list)
        users = self.getPostLikers(post_link)
        c_users = 0
        for u in users.keys():
            c_users+=1
            print("Getting gata for user: ", str(c_users))
            links_u_posts = self.getLinksForUsersPosts(users[u], 21)
            for p in links_u_posts:
                p_hashtag_list = self.findHashtagsInPost(p)
                for h in p_hashtag_list:
                    hashfield.addHashTag(h)
                    hashfield.addRelHashTags(h, p_hashtag_list)
