#!python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from threading import Thread
import pandas
from util import util
import time

class Crawler:    
    def __init__(
        self,
        # general
        urls,
        save_to = 'test.csv',
        
        # xpath
        td_xpath = None,
        field_xpath = {
            'name': './div[1]',
            'address': './div[3]',
            'phone': './div[4]',
        },
        next_xpath = None,

        # time (in second)
        delay_time = 3,
        loop_time = 30,
        wait_td_time = 25,
        wait_a_next_time = 2.5,
        
        # optional
        threads = 10,
        headless = True
    ):
        # general
        self.__urls = urls
        self.__save_to = save_to
        
        # xpath
        self.__td_xpath = td_xpath
        self.__next_xpath = next_xpath
        self.__field_xpath = field_xpath
        
        self.__threads = threads
        
        # time (in second)
        self.__delay_time = delay_time
        self.__loop_time = loop_time
        self.__wait_td_time = wait_td_time
        self.__wait_a_next_time = wait_a_next_time
        
        # private
        self.__items = {}
        self.__length = len(self.__urls)
        self.__token = int(self.__length / self.__threads)
        self.__threads = self.__threads if self.__threads <= self.__length else self.__length
        self.__headless = headless
        
    def run(self):
        threads = []
        
        for i in range(0, self.__threads):
            start = i * self.__token
            end = 0
            if i == self.__threads - 1:
                end = self.__length
                threads.append(
                    Thread(
                        target=self.__worker,
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
                    
                self.__save(self.__save_to)
                
            else:
                end = start + self.__token
                threads.append(
                    Thread(
                        target=self.__worker,
                        kwargs={
                            'start': start,
                            'end': end
                        }
                    )
                )

    def __worker(self, start, end):
        print(f'--- running ({start}, {end})')
        
        global items

        key = str(start)
        options = webdriver.ChromeOptions()
        if self.__headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        for i in range(start, end):
            link = self.__urls[i]
            print(f'{util.now()}: {link}')
            
            driver.get(link)
            time.sleep(self.__delay_time)
            round = 0
            
            start_time = int(time.time())
            
            while True:
                try:
                    td_error = False
                    if self.__td_xpath:
                        wait = WebDriverWait(driver, self.__wait_td_time)
                        wait.until(lambda d: d.find_elements(By.XPATH, self.__td_xpath))
                        tds = driver.find_elements(By.XPATH, self.__td_xpath)
                    else:
                        tds = [driver]
                    
                    for j in range(0, len(tds)):
                        _id = str(i + j) + driver.page_source
                        td = tds[j]
                        
                        try:
                            obj = {}
                            website = ''

                            for key in self.__field_xpath:
                                xpath = self.__field_xpath[key]
                                selector = td.find_element(By.XPATH, xpath)
                                content = util.get_content(link, selector)
                                text = util.content_to_text(content)
                                
                                obj[key] = text
                                
                                if content['link'] and website == '':
                                    website = content['link']
                                    
                            obj['website'] = website
                            obj['_id'] = _id
                            
                            if not key in self.__items:
                                self.__items[key] = []
                            
                            if not (
                                util.find(
                                    lambda each: each['_id'] == _id,
                                    self.__items[key]
                                )
                            ):
                                self.__items[key].append(obj)
                            
                        except:
                            td_error = True
                            pass
                    
                    if (
                        not td_error or
                        int(time.time()) - start_time >= self.__loop_time
                    ):
                        start_time = int(time.time())
                        if self.__next_xpath:
                            a_next = driver.find_element(By.XPATH, self.__next_xpath)
                            a_next.click()
                            
                        else:
                            break

                except:
                    try:
                        if self.__next_xpath:
                            wait = WebDriverWait(driver, self.__wait_a_next_time)
                            wait.until(lambda d: d.find_elements(By.XPATH, self.__next_xpath))
                            a_next = driver.find_element(By.XPATH, self.__next_xpath)
                            a_next.click()
                            
                        else:
                            break

                    except:
                        break
            
            if i == end - 1:
                driver.close()

    def __save(self, path):
        streams = []
        
        for key in self.__items:
            streams += self.__items[key]
        
        columns = self.__columns(streams[0])
        frame = pandas.json_normalize(streams)
        frame.to_csv(path, index=False, columns=columns)
        
        print('------------------- done \n')
        print(f'length: {len(streams)}')
        print('\n-------------------')
        
    def __columns(self, obj):
        columns = list(obj.keys())
        columns = list(filter(lambda each: each != '_id', columns))
        return columns
