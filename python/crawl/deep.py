#!python3

from util.crawler import Crawler
from selenium.webdriver.common.by import By
import re

# 0 - 118
# 118 - 168
def generate_urls(start, end):
    urls = []
    
    for i in range(start, end):
        urls.append(f'https://www.mirasapo.jp/subsidies?page={i + 1}')
    
    return urls

def robot_page(driver):
    try:
       robot = driver.find_element(By.XPATH, '//div[@id="captcha-container"]')
       if robot:
           return True
       
    except:
        pass
    
    return False

field_xpath = {
    'Title':        '//div[@class="main-header"]/h1',
    'Description':  '//div[@class="description full-text"]',
    'Expired Date': '//div[@class="overview-footer"]/div[1]/div[1]/div[1] /span[2]',
    'Difficulty':   '//div[@class="overview-footer"]/div[1]/div[2]/div[1] /span[2]',
    'Address':      '//div[@class="overview-footer"]/div[2]/div[1]',
    'Type':         '//div[@class="overview-footer"]/div[2]/div[2]',
    'Allowance':    '//div[@class="overview-footer"]/div[3]/div[2]',
    
    '実施機関':       '//table[@class="data-table"]//tr[1]/td',
    '上限金額':       '//table[@class="data-table"]//tr[2]/td',
    '公募期間':       '//table[@class="data-table"]//tr[3]/td',
    '対象者':         '//table[@class="data-table"]//tr[4]/td',
    '業種':          '//table[@class="data-table"]//tr[5]/td',
    '都道府県':       '//table[@class="data-table"]//tr[6]/td',
    '対象地域':       '//table[@class="data-table"]//tr[7]/td',
    '補足':          '//table[@class="data-table"]//tr[8]/td',
    
    '対象者-2':       '//div[@class="main-data-detail"]/div[1]/div',
    '対象費用':       '//div[@class="main-data-detail"]/div[2]/div',
    
    'More':        '//div[@class="data-buttons"]/a[@class="link"]'
}

a = Crawler(
    headless = False,
    urls_start = generate_urls(118, 122),
    next_xpath = '//a[@class="card-link"]',
    field_xpath = field_xpath,
    detail_page = lambda driver: True if re.match(r'.*/subsidy/[0-9]+.*', driver.current_url) else False,
    robot_page = robot_page,
    exit_wait=10000,
    threads=4,
    filter_items=False,
    save_to='test-3.csv',
)
# [
#         'https://www.mirasapo.jp/subsidies?page=2'
#     ]
a.run()