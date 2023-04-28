#!python3
from threading import Thread
from requests_html import HTML
import pandas
import requests
import json
import re
import jellyfish

values = pandas.read_csv('test/areas.csv').values
flow = 500
token = int(len(values) / flow)
threads = []
depends = [    
    '情報はありません',
    '掲載されている情報はありません',
    '現在、掲載されている情報はありません',
    '情報がありません',
    '情報はないです',
]

def similar(depends, target):
    trues = 0
    radio = 0.5
    percent = 0.3
    
    for depend in depends:
        s1 = jellyfish.jaro_similarity(depend, target)
        s2 = jellyfish.jaro_winkler_similarity(depend, target)
        
        if (s1 + s2) / 2 >= radio:
            trues += 1
    
    return trues / len(depends) >= percent

def h1_text(content):
    html = HTML(html=content)
    text_list = html.xpath('//body//h1//text()')
    text = ' '.join(text_list)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def save_to(save_path):
    f = open(save_path, "w")
    f.write(
        json.dumps(
            depends,
            ensure_ascii=False,
            indent=4
        )
    )
    f.close()
    
    print('\n--- done ---')
    print('length = ', len(depends))
    print('-------------\n')

def worker(start, end):
    for i in range(start, end):
        url = values[i][2]
        
        if type(url) == str and 'http' in url:
            try:
                invalid_url = url #+ 'soatraSSccaacc'
                print(f'\n+++ getting {invalid_url} +++\n')
                response = requests.get(invalid_url)
                response.encoding = response.apparent_encoding
                html = response.text
                html = HTML(html=html)
                text_list = html.xpath('//body//*[self::h1 or self::p[@class="no-data"]]//text()')
                
                for text in text_list:
                    text = re.sub(r'\s+', ' ', text).strip()
                    
                    if text and similar(depends, text):
                        if not text in depends:
                            depends.append(text)
                            print(f'\n -> append = {text} \n',)
                
            except:
                pass
        
def main():
    for i in range(0, flow):
        start = i * token
        
        if i == flow - 1:
            end = len(values)
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
                
            save_to('test-no.py')

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
        
if __name__ == '__main__':
    main()
    # words = [
    #     'apple',
    #     'app',
    #     'pple'
    # ]
    
    # f = similar(words, 'apple')
    # print(f)
