#!python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from threading import Thread
import pandas
from util import util
import time

same_url_wait = 3

class Crawler:    
    def __init__(
        self,
        # general
        urls_start,
        save_to = 'test.csv',
        filter_items = True,
        
        # 
        detail_page = lambda driver: bool(True),
        robot_page = lambda driver: bool(False),
        filter_work = lambda items, _id: not util.find(lambda each: each['_id'] == _id, items),
        
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
        wait_a_next_time = 1,
        exit_wait = 0,
        page_load_timeout = 6.5,
        
        # optional
        threads = 10,
        headless = True,
    ):
        # general
        self.__urls_start = urls_start
        self.__save_to = save_to
        self.__filter_items = filter_items
        
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
        self.__exit_wait = exit_wait
        self.__page_load_timeout = page_load_timeout
        
        # private
        self.__items = {}
        self.__length = len(self.__urls_start)
        self.__threads = self.__threads if self.__threads <= self.__length else self.__length
        self.__token = int(self.__length / self.__threads)
        self.__headless = headless
        
        # 
        self.__detail_page = detail_page
        self.__robot_page = robot_page
        self.__filter_work = filter_work
        
    def run(self):
        threads = []
        
        for i in range(0, self.__threads):
            start = i * self.__token
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
                time.sleep(self.__exit_wait)
                
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
        self.__items[key] = []
        items = self.__items[key]
        
        driver = self.__create_driver()
        
        for i in range(start, end):
            driver = self.__get_url(driver, self.__urls_start[i])
            time.sleep(self.__delay_time)
            loop_urls = []
            
            self.__deep_worker(
                driver,
                items,
                None,
                loop_urls,
            )
                
    def __deep_worker(self, driver , items, prev_source, loop_urls):        
        start_time = int(time.time())
        
        while self.__robot_page(driver):
            try:
                util.alert_sound('Reach robot page')
            except:
                pass
            
            time.sleep(3)
        
        while driver.current_url in loop_urls:
            if util.time_passed(start_time, same_url_wait):
                try:
                    driver.back()
                except:
                    pass
                return
            
            time.sleep(2)
        
        # print(f'{util.now()}: {driver.current_url}')
        
        loop_urls.append(driver.current_url)
        start_time = int(time.time())
        
        while prev_source == driver.page_source:
            if util.time_passed(start_time, 8):
                return
            
            time.sleep(2)
            
        while self.__robot_page(driver):
            try:
                util.alert_sound('Reach robot page')
            except:
                pass
            time.sleep(3)
            
        start_time = int(time.time())
        
        while True:
            try:
                error_td = False
                
                if self.__td_xpath:
                    wait = WebDriverWait(driver, self.__wait_td_time)
                    wait.until(lambda d: d.find_elements(By.XPATH, self.__td_xpath))
                    tds = driver.find_elements(By.XPATH, self.__td_xpath)

                else:
                    tds = [driver]
                
                if (
                    not self.__detail_page(driver) or
                    len(tds) == 0
                ):
                    if self.__next_xpath:
                        self.__next_click(driver, items, loop_urls)
                        
                    else:
                        try:
                            driver.back()
                        except:
                            pass

                    break
                
                else:
                    for td in tds:
                        _id = str(td) if self.__td_xpath else driver.page_source
                        
                        try:
                            obj = {}
                            website = ''

                            for key in self.__field_xpath:
                                xpath = self.__field_xpath[key]
                                selector = td.find_element(By.XPATH, xpath)
                                content = util.get_content(driver.current_url, selector)
                                text = util.content_to_text(content)
                                
                                obj[key] = text
                                
                                if content['link'] and website == '':
                                    website = content['link']
                                    
                            obj['website'] = website
                            obj['_id'] = _id
                            
                            if self.__filter_items:
                                if self.__filter_work(items, _id):
                                    items.append(obj)

                            else:
                                items.append(obj)
                            
                        except:
                            error_td = True
                            pass
                    
                    if (
                        not error_td or
                        util.time_passed(start_time, self.__loop_time)
                    ):
                        start_time = int(time.time())
                        
                        if self.__next_xpath:
                            self.__next_click(driver, items, loop_urls)
                            
                        else:
                            try:
                                driver.back()
                            except:
                                pass

                        break
                    
                time.sleep(1)

            except:
                if self.__next_xpath:
                    self.__next_click(driver, items, loop_urls)
                
                else:
                    try:
                        driver.back()
                    except:
                        pass
                    
                break

    
    def __next_click(self, driver, items, loop_urls):
        try:
            wait = WebDriverWait(driver, self.__wait_a_next_time)
            wait.until(lambda d: d.find_elements(By.XPATH, self.__next_xpath))
            a_nexts = driver.find_elements(By.XPATH, self.__next_xpath)

            i = 0
            while i < len(a_nexts):
                a_next = a_nexts[i]
                
                try:
                    current_url = driver.current_url
                    prev_source = driver.page_source
                    a_next.click()
                    
                    print(f'\n+++ url = {current_url} to next i = {i}')
                    print(f'+++ length = {len(a_nexts)}\n')
                    
                    self.__deep_worker(
                        driver,
                        items,
                        prev_source,
                        loop_urls
                    )

                except:
                    try:
                        a_nexts = driver.find_elements(By.XPATH, self.__next_xpath)
                    except:
                        pass
                    
                    i -= 1
                    
                    time.sleep(1)

                i += 1

        except:
            pass
        
        try:
            driver.back()
        except:
            pass
        
    def __save(self, path):
        streams = []
        
        try:
            for key in self.__items:
                streams += self.__items[key]
            
            columns = self.__columns(streams[0])
            frame = pandas.json_normalize(streams)
            frame.to_csv(path, index=False, columns=columns)
            
        except:
            pass
        
        print('------------------- done \n')
        print(f'length: {len(streams)}')
        print('\n-------------------')
        
    def __columns(self, obj):
        columns = list(obj.keys())
        columns = list(filter(lambda each: each != '_id', columns))

        return columns
    
    def __get_url(self, driver, url):
        while True:
            try:
                driver.set_page_load_timeout(self.__page_load_timeout)
                driver.get(url)
                break
            
            except:
                try:
                    if driver.current_url != 'data:,':
                        break
                    
                    else:
                        while True:
                            try:
                                driver.quit()
                                driver = self.__create_driver()
                                break
                            
                            except:
                                time.sleep(1)
                            
                except:
                    while True:
                        try:
                            driver.quit()
                            driver = self.__create_driver()
                            break
                        
                        except:
                            time.sleep(1)
        
        driver.set_page_load_timeout(1000000)
        
        return driver

    def __create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        if self.__headless:
            options.add_argument("--headless")
            
        driver = webdriver.Chrome(options=options)
        
        return driver
