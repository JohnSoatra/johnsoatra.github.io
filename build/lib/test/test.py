#!python3
from util import util

lis = [
    {
        'name': 'Soatra',
        'age': 20
    },
    {
        'name': 'keang',
        'age': 30
    }
]


a = util.find(lambda item: item['name'] == 'Soatra', lis)

print(a)
