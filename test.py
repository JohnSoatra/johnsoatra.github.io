#!python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from util import util
import time


driver = webdriver.Chrome()

def say(text):
    for i in range(0, 5):
        util.alert_sound(text)

for i in range(0, 1000):
    driver.get('https://www.mirasapo.jp/subsidies?page=2')
    
    try:
        driver.find_element(By.XPATH, '//div[@id="captcha-container"]')
        say('In Robot Page')
        break

    except:
        pass

time.sleep(10000)