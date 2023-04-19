#!python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from threading import Thread
import time
import pandas

read_file = 'test2.csv'
save_file = 'test.html'

f = open(save_file, 'w')
f.write('')
f.close()
f = open(save_file, 'a')

reader = pandas.read_csv(read_file)


def worker(driver, last):
    try:
        wait = WebDriverWait(driver, 30)
        wait.until(lambda d: d.find_elements(By.XPATH, '//table[@id="kyotenListTable"]//tr'))
        trs = driver.find_elements(By.XPATH, '//table[@id="kyotenListTable"]//tr')
        
        for tr in trs:
            text = tr.get_attribute('outerHTML')
            f.write(text)

        button = driver.find_element(By.XPATH, '//table[@id="kyotenListHeader"]//a[text()="次へ"]')
        button.click()
        
        worker(driver, last)
        
    except:
        try:
            button = driver.find_element(By.XPATH, '//table[@id="kyotenListHeader"]//a[text()="次へ"]')
            worker(driver, last)

        except:
            driver.close()
            if last:
                f.close()
                print('done')

def main():
    threads = []
    thread_length = 50
    
    for i in range(0, len(reader.values)):
        record = reader.values[i]
        link = record[0]
        last = i == len(reader.values) - 1
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        thread = Thread(
            target = worker,
            kwargs = {
                'driver': driver,
                'last': last
            }
        )
        thread.start()
        threads.append(thread)
    
        if len(threads) == thread_length:
            for each in threads:
                each.join()
            threads = []

    time.sleep(1000000)

if __name__ == '__main__':
    main()