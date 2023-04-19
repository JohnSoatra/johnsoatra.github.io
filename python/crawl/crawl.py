#!python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from threading import Thread
import pandas
from util import util
import time

reader = pandas.read_csv('csv/test2.csv')
length = len(reader.values)
amount = 10
amount = amount if amount <= length else length
token = int(length / amount)
items = {}
delay = 5
loop_time = 30
wait_td_time = 30
wait_btn_time = 3
            
def main():
    threads = []
    
    for i in range(0, amount):
        start = i * token
        end = 0
        if i == amount - 1:
            end = length
            threads.append(
                Thread(
                    target=worker,
                    kwargs={
                        'start': start,
                        'end': end
                    }
                )
            )
            for thread in threads:
                thread.start()
                
            for thread in threads:
                thread.join()
        else:
            end = start + token
            threads.append(
                Thread(
                    target=worker,
                    kwargs={
                        'start': start,
                        'end': end
                    }
                )
            )

def worker(start, end):
    print(f'--- running ({start}, {end})')
    
    global items

    key = str(start)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    for i in range(start, end):
        link = reader.values[i][0]
        print(f'{util.now()}: {link}')
        
        driver.get(link)
        time.sleep(delay)
        
        start_time = int(time.time())
        
        while True:
            try:
                td_error = False
                wait = WebDriverWait(driver, wait_td_time)
                wait.until(lambda d: d.find_elements(By.XPATH, '//table[@id="kyotenListTable"]//tr/td'))
                tds = driver.find_elements(By.XPATH, '//table[@id="kyotenListTable"]//tr/td')
                
                for td in tds:
                    try:
                        name = td.find_element(By.XPATH, './*[1]')
                        address = td.find_element(By.XPATH, './*[3]')
                        phone = td.find_element(By.XPATH, './*[4]')
                        website = name.find_element(By.XPATH, './a').get_attribute('href')
                        
                        obj = {
                            "name": name.text,
                            "address": address.text,
                            "phone": phone.text,
                            "website": website
                        }
                        
                        if not key in items:
                            items[key] = []
                        
                        if not util.find(
                            lambda each: each['website'] == obj['website'],
                            items[key]
                        ):
                            items[key].append(obj)
                        
                        print(obj)
                        
                    except:
                        td_error = True
                        pass
                
                if not td_error or int(time.time()) - start_time >= loop_time:
                    start_time = int(time.time())
                    button = driver.find_element(By.XPATH, '//table[@id="kyotenListHeader"]//a[text()="次へ"]')
                    button.click()

            except:
                try:
                    wait = WebDriverWait(driver, wait_btn_time)
                    wait.until(lambda d: d.find_elements(By.XPATH, '//table[@id="kyotenListHeader"]//a[text()="次へ"]'))
                    button = driver.find_element(By.XPATH, '//table[@id="kyotenListHeader"]//a[text()="次へ"]')

                except:
                    break
        
        if i == end - 1:
            driver.close()

def save(path):
    stream = []
    
    for key in items:
        stream += items[key]
    
    frame = pandas.json_normalize(stream)
    frame.to_csv(path, index=False)
    
    print('------------------- done \n')
    print(f'length: {len(stream)}')
    print('\n-------------------')

if __name__ == '__main__':
    main()
    save('save.csv')