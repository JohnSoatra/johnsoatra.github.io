#!python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

a = webdriver.Chrome()
a.set_page_load_timeout(0)
a.get('https://www.mirasapo.jp/subsidies?page=2')
    

print('done')

time.sleep(10000)