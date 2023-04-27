#!python3
import os
import pandas

def combine(folder, save_to):
    lt_name = os.listdir(folder)
    path_names = []
    
    for name in lt_name:
        path_names.append(f'{folder}/{name}')
    
    sum = pandas.concat(
        map(pandas.read_csv, path_names),
        ignore_index=True
    )
    
    sum.to_csv(save_to, index=False)
    print('--- done ---')

combine('files', 'last.csv')