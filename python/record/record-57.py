#!python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
import time

def clicker(driver):
    try:
        wait = WebDriverWait(driver, 20)
        wait.until(lambda d: d.find_element(By.XPATH, '//button[@class="m-read-more u-hover"]'))
        
        button = driver.find_element(By.XPATH, '//button[@class="m-read-more u-hover"]')
        button.click()
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'{current_time}: clicking')
        
        clicker(driver)
        
    except:
        # driver.close()
        print('\n--- done ---\n')

def main():
    url = 'https://itp.ne.jp/keyword/?keyword=%E4%BF%9D%E9%99%BA%E4%BB%A3%E7%90%86%E5%BA%97&sort=01&sbmap=false'
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=option)
    driver.get(url)
    button = driver.find_element(By.XPATH, '//button[@class="o-result-control__sort__list__item__button is-active"]')
    button.click()
    
    clicker(driver)
    
    time.sleep(100000)

if __name__ == '__main__':
    main()