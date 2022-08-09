import time
import requests
import os
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options


def Num_of_Seasons(driver):
    for i in range(1, 19):
            try:
                season = driver.find_element(By.XPATH,value=r'/html/body/div[1]/section[1]/div[2]/div/div[2]/ul[1]/li[' + str(i) + ']')
            except:
                return i

def Num_of_Episodes(driver):
    for i in range(1, 39):
        try:
            episode = driver.find_element(By.XPATH,value=r'/html/body/div[1]/section[1]/div[2]/div/div[2]/ul[2]/li[' +str(i) + ']')
        except:
            return i

def Crawler():
    ShowName = input("Input show name:")
    #ShowName ="The+Office"

    Option = Options()
    Options.headless = True
    driver = webdriver.Firefox(options=Options)

    URL = "https://sdarot.tw/search?term="
    URL += ShowName
    URL.replace(r' ',"+")

    driver.get(URL)
    driver.maximize_window()
    Show = driver.find_element(By.XPATH,value="/html/body/div/section/div[2]/div/div[1]")

    ActionChains(driver).move_to_element(Show).click().perform()
    Showbtn = driver.find_element(By.XPATH,value="/html/body/div/section/div[2]/div/div[1]/div/a")

    driver.get(Showbtn.get_attribute("href"))


    os.makedirs(ShowName, exist_ok=True)
    Seasons = Num_of_Seasons(driver)
    for i in range(1,Seasons):
        os.makedirs(ShowName+"/Season "+str(i), exist_ok=True)
        season = driver.find_element(By.XPATH,value=r'/html/body/div[1]/section[1]/div[2]/div/div[2]/ul[1]/li[' + str(i) + ']')
        driver.find_element(By.XPATH, value=r'/html/body/div[1]/section[1]/div[2]/div/div[2]/ul[1]/li[' + str(i) + ']/a').click()

        EpisodesInSeason = Num_of_Episodes(driver)
        for j in range(1,EpisodesInSeason):

            #episode = driver.find_element(By.XPATH,value=r'/html/body/div[1]/section[1]/div[2]/div/div[2]/ul[2]/li[' +str(j) + ']') delete maybe?


            driver.find_element(By.XPATH, value=r'/html/body/div[1]/section[1]/div[2]/div/div[2]/ul[2]/li[' +str(j) + ']/a').click()
            time.sleep(40)

            driver.find_element(By.XPATH, value= r'//*[@id="proceed"]').click()
            cookies = driver.get_cookies()
            s = requests.Session()
            for cookie in cookies:
                s.cookies.set(cookie['name'], cookie['value'])
            Video = driver.find_element(By.XPATH, value= r'//*[@id="videojs_html5_api"]')
            VideoLink = Video.get_attribute("src")
            Video = s.get(VideoLink, allow_redirects=True)

            path=ShowName+"/Season "+str(i)+"/Episode "+str(j)+".mp4"

            open(path, 'wb').write(Video.content)










if __name__ == '__main__':
    Crawler()