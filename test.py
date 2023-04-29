#!python3
from threading import Thread
from zchecker import eyes
import pandas
import json

read_from = 'test.csv'
write_to = 'inactive-active.json'

values = pandas.read_csv(read_from).values
flow = 50
token = int(len(values) / flow)
threads = []
founds = []

def save_file():
    f = open(write_to, "w")
    f.write(
        str(founds)
        # json.dumps(
        #     founds,
        #     ensure_ascii=False,
        #     indent=4
        # )
    )
    f.close()
    
    print('\n--- done ---')
    print('length = ', len(founds))
    print('-------------\n')

def worker(start, end):
    for i in range(start, end):
        url = values[i][2]
        
        if type(url) == str and 'http' in url:
            try:
                obj = eyes.view_page(url)
                if obj['active']:
                    print(f'\n+++ active +++ {url}\n')
                    founds.append(obj)
                    
                else:
                    print(f'--- inactive --- {url}')
                    # return
                
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
                
            save_file()

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
