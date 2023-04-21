#!python3
from util import util
import time
from datetime import datetime
import calendar

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


current_GMT = time.gmtime()

time_stamp = calendar.timegm(current_GMT)
print(time.time())
print(time_stamp)