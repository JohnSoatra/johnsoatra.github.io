#!python3
from zchecker.checker import active_url
from threading import Thread
import pandas

values = pandas.read_csv('inactive.csv').values
flow = 1000
token = int(len(values) / flow)
threads = []
points = 0
checks = 0

def last_work():
    print('\n--- Done ---')
    print('points = ', points)
    print('checks = ', checks)
    print('average = ', points / checks)
    print('\n-----------')

def worker(start, end):
    global points
    global checks
    
    for i in range(start, end):
        url = values[i][2]
        
        if type(url) == str and 'http' in url:
            obj = active_url(url)
            print(f'\n +++ result: {obj}-- {url} +++ \n')
            if not obj['active'] and obj['checked']:
                point = obj['point']
                points += point
                checks += 1
        
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
                
            last_work()

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
