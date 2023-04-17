#!python3
# import parallelTestModule
from threading import Thread
import time
import multiprocessing

def fun(i):
    time.sleep(2)
    print('i = ', i)

def main():
    processes = []

    for i in range(0, 4):
        process = multiprocessing.Process(
            target = fun,
            kwargs = {
                'i': i
            }
        )
        process.start()
        processes.append(process)


if __name__ == '__main__':
    main()
    # processes = []

    # def fun(i):
    #     time.sleep(2)
    #     print('i = ', i)

    # for i in range(0, 4):
    #     process = multiprocessing.Process(
    #         target = lambda: print('f'),
    #         kwargs = {
    #             'i': i
    #         }
    #     )
    #     process.start()
    #     processes.append(process)
    
    # for process in processes:
    #     process.join()
