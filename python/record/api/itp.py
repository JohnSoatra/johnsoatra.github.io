#!python3
import requests
import pandas
from util import util
from threading import Thread
import time
import asyncio

completed = 0
items = []
amount = 50
token = int(2000 / amount)

def main():
    def api(index):
        return f'https://itp.ne.jp/search?size=1&from={index}&kw=%E4%BF%9D%E9%99%BA%E4%BB%A3%E7%90%86%E5%BA%97'

    def append(record):
        items.append(record)

    def runner(start=0, end=0, forever=False):
        print(f'runner ({start}, {end})')
        global completed
        counter = start
        
        while counter < end or forever:
            response = requests.get(api(counter))
            time.sleep(5)
            print('res = ', response)
            obj = response.json()
            
            if len(obj['hits']['hits']):
                print(f'{util.now()}: getting -- runner ({start}, {end})')
                hit = obj['hits']['hits'][0]
                ki = hit["_source"]["ki"]
                record = {
                    "name": ki["name"],
                    "stations": " / ".join(list(map(lambda each: each["name"], ki["n_station"]))),
                    "phone": ki["tel1"],
                    "address": ki["jusyo"] + ki["jyusyo_banti"],
                    "website": ki["url"]
                }
                print(record)
                append(record)
                # asyncio.run(append(record))

            else:
                break
            
            counter += 1
    
    threads = []

    for i in range(0, amount):
        start = i * token
        if i == amount - 1:
            threads.append(
                Thread(
                    target=runner,
                    kwargs={
                        "start": start,
                        "forever": True
                    }
                )
            )
            for thread in threads:
                thread.start()
        
            for thread in threads:
                thread.join()

        else:
            threads.append(
                Thread(
                    target=runner,
                    kwargs={
                        "start": start,
                        "end": start + token
                    }
                )
            )

if __name__ == '__main__':
    main()
    df = pandas.json_normalize(items)
    df.to_csv('test.csv', index=False)
    print('------------------- done \n')
    print(f'--- length: {len(items)} ---')
    print('\n-------------------')
